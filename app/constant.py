# -*- coding: utf-8 -*-
from __future__ import annotations

import os

from enum import StrEnum
from pydantic import BaseModel


class Constant(StrEnum):
    POLYGON_API_KEY = os.environ["POLYGON_API_KEY"]
    FINNHUB_API_KEY = os.environ["FINNHUB_API_KEY"]


class Message(BaseModel):
    message: str
