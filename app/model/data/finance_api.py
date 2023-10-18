# -*- coding: utf-8 -*-
from pydantic import BaseModel


class FinnHubOutput(BaseModel):
    close: list[int | float]
    open: list[int | float]
    high: list[int | float]
    low: list[int | float]
    volumn: list[int | float]
    api_status: str
    time: list[str]
