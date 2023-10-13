# -*- coding: utf-8 -*-
from model.finnhub import FinnHubAPI

obj = FinnHubAPI()
response = obj.pull_data(("AAPL", "TSLA"), "2021-10-05", "2022-10-05")
