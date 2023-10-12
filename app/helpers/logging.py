# -*- coding: utf-8 -*-
"""Sending logging via webhooks to discord."""
from __future__ import annotations

import asyncio
import itertools
import logging
import textwrap
import time
import traceback
from collections import defaultdict
from contextlib import suppress
from enum import Enum
from typing import DefaultDict, Dict, List, Optional

import aiohttp
import discord
from discord.utils import utcnow

from .embed import EmbedListBuilder
from .utility import Utility


class LogColor(Enum):
    """Color of LogRecord to be used in an embed."""

    DEFAULT = 0x369551
    INFO = 0x369551
    DEBUG = 0x808080
    WARNING = 0xDDBE81
    ERROR = 0xD5658A
    CRITICAL = 0xC25558

    @staticmethod
    def get_color(levelname: str) -> int:
        """Get color based on levelname of a LogRecord."""
        if hasattr(LogColor, levelname):
            return getattr(LogColor, levelname).value
        return LogColor.DEFAULT.value


class WebhookHandler(logging.StreamHandler):
    """A queue of logs."""

    logger = logging.getLogger("WebhookHandler")

    def __init__(self, webhook_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue: List[logging.LogRecord] = []
        self._filters: DefaultDict[str, list] = defaultdict(list)
        self.webhook_url = webhook_url
        self.webhook = None

    def emit(self, record: logging.LogRecord) -> None:
        """Add records into the queue."""
        try:
            self.add(record)
        except Exception as error:  # pylint: disable=broad-except
            self.logger.exception(self.format_exception(error))
            self.handleError(record)

    @staticmethod
    def format_exception(error: Exception) -> str:
        """Format the error traceback into a string."""
        return "".join(traceback.format_exception(type(error), error, error.__traceback__))

    @staticmethod
    def create(webhook_url: str, filters: Optional[Dict[str, List[str]]] = None) -> WebhookHandler:
        """A method to create a WebhookHandler that will send logs using the send_method."""
        handler = WebhookHandler(webhook_url)

        if filters:
            for levelname, names in filters.items():
                for name in names:
                    handler.add_filter(levelname, name)

        return handler

    def add_filter(self, levelname: str, name: str) -> None:
        """Add a filter."""
        self._filters[levelname].append(name)

    def remove_filter(self, levelname: str, name: str) -> None:
        """Remove a filter."""
        with suppress(ValueError):
            self._filters[levelname].remove(name)

    def _pass_filter(self, record: logging.LogRecord) -> bool:
        """Check if a record pass all filters."""
        return record.name not in self._filters[record.levelname]

    def add(self, record: logging.LogRecord) -> None:
        """Add a record to the queue if it passes all filters."""
        if self._pass_filter(record):
            self._queue.append(record)

    async def _send(self, session: aiohttp.ClientSession, embeds: List[discord.Embed]) -> None:
        if not embeds:
            return

        webhook = discord.Webhook.from_url(self.webhook_url, session=session)
        for _embeds in Utility.chunk_embeds(embeds):
            started = time.perf_counter()
            await webhook.send(embeds=_embeds)
            await asyncio.sleep(1 - (time.perf_counter() - started))

    @staticmethod
    def _get_record_message(record: logging.LogRecord) -> str:
        with suppress(AttributeError):
            return record.message

        with suppress(AttributeError, TypeError):
            return record.msg % record.args

        with suppress(AttributeError):
            return record.msg

    @staticmethod
    def _get_record_name(record: logging.LogRecord) -> str:
        try:
            # Loguru added the original record name in the `extra` attribute.
            # See `bot\__init__.py:36`
            return record.extra["name"]
        except (AttributeError, KeyError):
            return record.name

    async def _emit(self, session: aiohttp.ClientSession) -> None:
        if not self._queue:
            return

        try:
            embeds: List[discord.Embed] = []
            for levelname, queues in itertools.groupby(self._queue, key=lambda r: r.levelname):
                embed = discord.Embed(color=LogColor.get_color(levelname), timestamp=utcnow())
                embed.set_author(name=levelname)
                embeds_builder = EmbedListBuilder(base_embed=embed)
                for name, records in itertools.groupby(queues, key=self._get_record_name):
                    record_texts: List[str] = []
                    for record in records:
                        if text := self._get_record_message(record):
                            record_texts.append(text)
                        else:
                            self.logger.error("Record is weird\n%r", record)

                    messages = textwrap.wrap(
                        "\n".join(record_texts),
                        width=1000,
                        replace_whitespace=False,
                        break_on_hyphens=False,
                        break_long_words=False,
                    )

                    for message in messages:
                        embeds_builder.add_field(name=name, value=message, inline=False, wrap_code=True)
                embeds.extend(embeds_builder)
            await self._send(session, embeds)
        except Exception as error:  # pylint: disable=broad-except
            self.logger.exception(self.format_exception(error))
        else:
            # Only clear the queue if no internal error.
            self._queue.clear()

    async def clear_queue_async(self) -> None:
        """Periodically clear the queue every `wait_time` seconds, default 1."""
        async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
            # This will be run in a seperated thread.
            # To avoid asyncio raising errors for bounded lock in different threads, we need a new event loop.
            while True:
                if self._queue:
                    await self._emit(session)
                await asyncio.sleep(1)

    def clear_queue_threaded(self) -> None:
        """
        A blocking call that will clear the queue periodically.

        This should be called in a new thread.
        """
        asyncio.run(self.clear_queue_async())
