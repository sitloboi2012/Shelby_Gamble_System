# -*- coding: utf-8 -*-
from __future__ import annotations
from contextlib import suppress

import datetime
import time

from functools import lru_cache

import finnhub as fb

from finnhub.client import Client

from base import BaseFinanceAPI
from constant import Constant


class FinnHubAPI(BaseFinanceAPI):
    """`FinnHub API Object`. For documentation, please use this link: https://finnhub.io/docs/api"""

    def __init__(self, api_name: str = "FinnHub API", api_key: str = Constant.FINNHUB_API_KEY):
        super().__init__(api_name, api_key)
        self.api_name = api_name
        self.api_key = api_key

    @lru_cache
    def connect_api(self) -> Client:
        """
        Connects to the API using the provided API key and returns a Client object.

        Returns:
            Client: The connected API client.

        Example:
            ```python
            instance = ClassName()
            client = instance.connect_api()
            ```
        """
        with suppress(ValueError):
            return fb.Client(api_key=self.api_key)

    def pull_data_sync(self, ticker: str, from_date: int, to_date: int) -> dict:
        """
        Retrieves stock candle data for a given ticker symbol within a specified date range.

        Args:
            ticker (str): The ticker symbol for which to retrieve data.
            from_date (int): The starting date of the data range in UNIX timestamp format.
            to_date (int): The ending date of the data range in UNIX timestamp format.

        Returns:
            dict: The retrieved stock candle data.
        """
        return self.client.stock_candles(ticker, "D", from_date, to_date)

    @lru_cache
    def pull_data(
        self,
        ticker: str | list[str],
        from_date: str,
        to_date: str,
    ):
        """
        Retrieves stock candle data for a given ticker symbol or list of ticker symbols within a specified date range.

        Args:
            ticker (str | list[str]): The ticker symbol(s) for which to retrieve data.
            from_date (str): The starting date of the data range in the format 'YYYY-MM-DD'.
            to_date (str): The ending date of the data range in the format 'YYYY-MM-DD'.

        Returns:
            dict | list[dict]: The retrieved stock candle data. If a single ticker is provided, a dictionary is returned. If a list of tickers is provided, a list of dictionaries is returned.
        """
        from_date_unix = self.convert_date_to_unix(from_date)
        to_date_unix = self.convert_date_to_unix(to_date)

        if isinstance(ticker, list):
            return [self.pull_data_sync(name, from_date_unix, to_date_unix) for name in ticker]
        else:
            return self.pull_data_sync(ticker, from_date_unix, to_date_unix)

    @lru_cache
    def convert_date_to_unix(self, date: str) -> int:
        """
        Converts a date string in the format 'YYYY-MM-DD' to a UNIX timestamp.

        Args:
            date (str): The date string to convert.

        Returns:
            int: The UNIX timestamp corresponding to the input date.
        """
        date_split = date.split("-")
        date_obj = datetime.date(date_split[0], date_split[1], date_split[2])
        return int(time.mktime(date_obj.timetuple()))

    @lru_cache
    def convert_unix_to_date(self, unix_date: int) -> str:
        """
        Converts a UNIX timestamp to a date string in the format 'YYYY-MM-DD'.

        Args:
            unix_date (int): The UNIX timestamp to convert.

        Returns:
            str: The date string corresponding to the input UNIX timestamp.
        """
        return datetime.datetime.fromtimestamp(unix_date, tz=datetime.timezone.utc).strftime("%Y-%m-%d")
