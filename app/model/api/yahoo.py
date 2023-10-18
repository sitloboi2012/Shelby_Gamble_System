# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
import logging
from functools import lru_cache

import yfinance as yf

from .base import BaseFinanceAPI

MODULE_NAME = "YahooFinance_API"
logger = logging.getLogger(MODULE_NAME)


class YahooFinanceAPI(BaseFinanceAPI):
    def __init__(self, api_name: str = "Yahoo Finance API", api_key: str | None = None):
        super().__init__(api_name, api_key)
        self.api_name = api_name
        self.api_key = api_key

    @lru_cache
    def connect_api(self):
        return

    def pull_data(self, ticker: str, period: str = "30d"):
        info = yf.Ticker(ticker)
        history_data = info.history(period=period)
        clean_data = self.clean_data(history_data).to_dict("list")
        logger.info(f"Successfully pulling {ticker} from {datetime.datetime.now().date()} to {period} before")
        return clean_data

    def clean_data(self, response_data):
        response_data = response_data.reset_index()
        response_data["Date"] = response_data["Date"].dt.date

        return response_data
