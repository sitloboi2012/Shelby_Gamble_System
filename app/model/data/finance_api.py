# -*- coding: utf-8 -*-
import datetime

from pydantic import BaseModel


class FinanceAPIOutput(BaseModel):
    close: list[int | float]
    open: list[int | float]
    high: list[int | float]
    low: list[int | float]
    volumn: list[int | float]
    date: list[datetime.date] | list[str]
