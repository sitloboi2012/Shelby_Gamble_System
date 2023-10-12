# -*- coding: utf-8 -*-
from __future__ import annotations

from base import BaseFinanceAPI


class FinnHubAPI(BaseFinanceAPI):
    def __init__(self, api_name: str, api_key: str):
        super().__init__(api_name, api_key)
        self.api_name = api_name
        self.api_key = api_key
