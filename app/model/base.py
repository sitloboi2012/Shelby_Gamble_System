# -*- coding: utf-8 -*-
from __future__ import annotations
from abc import ABC, abstractmethod


class BaseFinanceAPI(ABC):
    def __init__(self, api_name: str, api_key: str | None):
        self.api_name = api_name
        self.api_key = api_key

    @abstractmethod
    def pull_data(self):
        pass

    @abstractmethod
    def clean_data(self):
        pass

    @abstractmethod
    def connect_api(self):
        pass

