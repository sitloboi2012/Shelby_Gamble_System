# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from enum import StrEnum

from pydantic import BaseModel


class Constant(StrEnum):
    FINNHUB_API_KEY = os.environ["FINNHUB_API_KEY"]
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]


class Message(BaseModel):
    message: str
