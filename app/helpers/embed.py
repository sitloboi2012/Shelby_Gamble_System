# -*- coding: utf-8 -*-
"""Utilities for building and modifying embeds."""
from __future__ import annotations

import textwrap
from copy import deepcopy
from typing import List

import discord
from discord.ext import commands


class EmbedLimits:
    """Definitions of discord embed size limits."""

    # Max length of all text in embed.
    OVERALL_LIMIT = 6000

    # Max length of description field.
    DESCRIPTION_LIMIT = 4096

    # Max length of an individual field.
    FIELD_VALUE_LIMIT = 1024

    # Max number of fields in an embed.
    FIELD_COUNT_LIMIT = 25


class EmbedListBuilder:
    """
    Utility class that allows building a list of embeds by adding content. Handles splitting off new embeds copied
    from a base embed as needed.

    Note that the copies of the original embed are a straight copy of the underlying embed dict. So stuff like
    description, fields, colors, etc. will all be copied.
    """

    __slots__ = ("base_embed", "copy_description", "embeds", "has_content", "field_count_limit")

    def __init__(
        self,
        base_embed: discord.Embed,
        copy_description: bool = False,
        *,
        field_count_limit: int = EmbedLimits.FIELD_COUNT_LIMIT,
    ) -> None:
        """Creates an EmbedListBuilder.

        Args:
            base_embed (discord.Embed): embed that will be copied for each new embed created
            copy_description (bool): if True, copied embeds will retain the original description
        """
        self.base_embed = base_embed
        self.copy_description = copy_description

        self.embeds: List[discord.Embed] = [deepcopy(base_embed)]
        self.has_content = False
        self.field_count_limit = field_count_limit

    @property
    def latest_embed(self) -> discord.Embed:
        """Gets the final embed in the list, which is always the one that stuff is added to."""
        return self.embeds[-1]

    def _new_embed(self):
        """Adds a new copy of the base embed to the list of embeds"""
        new_embed: discord.Embed = deepcopy(self.base_embed)
        if not self.copy_description:
            new_embed.description = None
        self.embeds.append(new_embed)

    def set_footer(self, text: str):
        """Sets the footer on all embeds in the builder.

        Note that this does not reflow embeds and may cause embeds to become too large.
        """
        for embed in self:
            embed.set_footer(text=text)

    def add_field(self, name: str, value: str, split_lines: bool = True, inline: bool = True, wrap_code: bool = False):
        # sourcery skip: assign-if-exp, extract-method, hoist-similar-statement-from-if, swap-nested-ifs
        """Adds a new field, generating a new embed as needed.

        While wrap_code will attempt to escape backticks, this may still result in extremely long embeds! Consider
        replacing backticks with another character that's not used in discord markdown for clarity.

        Args:
            name (str): field name
            value (str): string to put in the field
            split_lines (bool, optional): if True, will automatically split the string into multiple fields as needed
            inline (bool, optional): inline param for fields
            wrap_code (bool, optional): if True, the value will have backticks escaped and be wrapped in a code block
        """
        self.has_content = True

        # Escape backticks and wrap in code block.
        if wrap_code and split_lines:
            value = value.replace("`", "\\`")
        wrapped_value = f"```\n{value}\n```"

        total_len = len(wrapped_value) if wrap_code else len(value)

        if total_len > EmbedLimits.FIELD_VALUE_LIMIT:
            if not split_lines:
                raise ValueError("Value too long for a single field")

            # Value is too long, be nice and split it into multiple fields.

            lines = []

            if wrap_code:
                # Wrapping in codeblock takes 8 characters: 6 backticks and 2 newlines
                extra_len = 8
            else:
                # Wrapping by lines takes 1 newline
                extra_len = 1

            # Split the value into lines, wrapping lines where needed if too long.
            for line in value.splitlines():
                lines.extend(textwrap.wrap(line, width=EmbedLimits.FIELD_VALUE_LIMIT - extra_len))

            # Build field values, adding new field when necessary.
            curr_value = ""
            for line in lines:
                if len(curr_value) + extra_len + len(line) > EmbedLimits.FIELD_VALUE_LIMIT:
                    self.add_field(name, split_lines=False, value=curr_value, inline=inline, wrap_code=wrap_code)
                    curr_value = ""

                if wrap_code:
                    curr_value += line
                else:
                    curr_value += f"{line}\n"
            if curr_value:
                self.add_field(name, split_lines=False, value=curr_value, inline=inline, wrap_code=wrap_code)
        if wrap_code:
            value = wrapped_value

        if len(self.latest_embed.fields) == self.field_count_limit:
            # Latest embed has reached field limit, make a new one.
            self._new_embed()

        if len(self.latest_embed) + len(name) + len(value) > EmbedLimits.OVERALL_LIMIT:
            # Latest embed will reach length limit, make a new one.
            self._new_embed()

        # Add the field to the latest embed.
        self.latest_embed.add_field(name=name, value=value, inline=inline)

    def add_description_text(self, value: str):
        """Adds another chunk of text to the description. A newline will be added automatically."""
        self.has_content = True

        # 1 for the newline
        additional_length = 1 + len(value)

        if len(self.latest_embed.description) + additional_length > EmbedLimits.DESCRIPTION_LIMIT: # type: ignore
            # Latest embed has reached field limit, make a new one.
            self._new_embed()

        if len(self.latest_embed) + additional_length > EmbedLimits.OVERALL_LIMIT:
            # Latest embed will reach length limit, make a new one.
            self._new_embed()

        self.latest_embed.description += f"\n{value}" # type: ignore

    async def reply(self, ctx: commands.Context | discord.Message):
        """Convenience function that replies in a context with all of the embeds."""
        for embed in self:
            await ctx.reply(embed=embed)

    async def send(self, ctx: discord.abc.Messageable, content: str = None): # type: ignore
        """Send all embeds via a discord.abc.Messageable."""
        for embed in self:
            await ctx.send(content=content, embed=embed)

    def add_pagination(self, formatter: str = "{current}/{total}"):
        """Add pagination to all of the embeds."""
        for index, embed in enumerate(self.embeds, 1):
            embed.set_footer(text=formatter.format(current=index, total=len(self.embeds)))

    def __iter__(self):
        yield from self.embeds
