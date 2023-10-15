# -*- coding: utf-8 -*-
from __future__ import annotations
from contextlib import suppress

import datetime
import time

from functools import lru_cache

import streamlit as st
import finnhub as fb

from finnhub.client import Client

from .base import BaseFinanceAPI


class FinnHubAPI(BaseFinanceAPI):
    """`FinnHub API Object`. For documentation, please use this link: https://finnhub.io/docs/api"""

    def __init__(
        self,
        api_name: str = "FinnHub API",
        api_key: str = st.secrets["FINNHUB_API_KEY"],
    ):
        super().__init__(api_name, api_key)
        self.api_name = api_name
        self.api_key = api_key
        self.client_api = self.connect_api()

    @lru_cache
    def connect_api(self) -> Client:  # type: ignore
        """
        Connects to the API using the provided API key and returns a Client object.

        Returns:
            Client: The connected API client.
        """
        with suppress(ValueError):
            return fb.Client(api_key=self.api_key)

    def pull_data_sync(self, ticker: str, from_date: int, to_date: int) -> dict:
        """
        Retrieves stock candle data for a given ticker symbol
        within a specified date range.

        Args:
            ticker (str): The ticker symbol to retrieve data.
            from_date (int): The start date in UNIX timestamp format.
            to_date (int): The ending date in UNIX timestamp format.

        Returns:
            dict: The retrieved stock candle data.
        """
        return self.client_api.stock_candles(ticker, "D", from_date, to_date)

    @lru_cache
    def pull_data(
        self,
        ticker: str | tuple[str],
        from_date: str,
        to_date: str,
    ) -> dict[str, int | float | str] | list[dict[str, int | float | str]]:
        """
        Retrieves stock candle data for a given ticker symbol or list of
        ticker symbols within a specified date range.

        Args:
            ticker (str | list[str]): The ticker symbol(s) for which to retrieve data.
            from_date (str): The starting date in the format 'YYYY-MM-DD'.
            to_date (str): The ending date in the format 'YYYY-MM-DD'.

        Returns:
            dict | list[dict]: The retrieved stock candle data.
            If a single ticker is provided, a dictionary is returned.
            If a list of tickers is provided, a list of dictionaries is returned.
        """
        from_date_unix = self.convert_date_to_unix(from_date)
        to_date_unix = self.convert_date_to_unix(to_date)

        if not isinstance(ticker, tuple):
            response = self.pull_data_sync(ticker, from_date_unix, to_date_unix)
            return self.clean_data(response)

        result = []
        for name in ticker:
            response = {name: self.pull_data_sync(name, from_date_unix, to_date_unix)}
            result.append(response)
        return result

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
        date_obj = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
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

    def clean_data(self, response_dict):
        response_dict["close"] = response_dict["c"]
        response_dict["high"] = response_dict["h"]
        response_dict["low"] = response_dict["l"]
        response_dict["open"] = response_dict["o"]
        response_dict["volumn"] = response_dict["v"]
        response_dict["api_status"] = response_dict["s"]
        response_dict["time"] = response_dict["t"]
        del (
            response_dict["c"],
            response_dict["h"],
            response_dict["l"],
            response_dict["t"],
            response_dict["o"],
            response_dict["v"],
            response_dict["s"],
        )

        response_dict["time"] = [self.convert_unix_to_date(value) for value in response_dict["time"]]
        return response_dict
