# -*- coding: utf-8 -*-
from __future__ import annotations

import logging


from model.api.finnhub import FinnHubAPI
from helpers.utility import Utility
from constant import Message
from model.data.finance_api import FinnHubOutput

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

MODULE_NAME = "FinnHub"

unblock = Utility.unblock_custom(MODULE_NAME, max_workers=7)

router = APIRouter(prefix="/api/shelby-backend", tags=["FinnHub"])
logger = logging.getLogger(MODULE_NAME)

finnhub = FinnHubAPI()


@router.post(
    "/finnhub/pull-data",
    response_model=FinnHubOutput,
    responses={
        401: {"model": Message},
        500: {"model": Message},
    },
)
async def pulling_data(ticker: str = Form(..., description="Name of the ticker to pull data"), from_date: str = Form(..., description="Start date to pull"), end_date: str = Form(..., description="End date to pull")):
    response = await unblock(finnhub.pull_data, ticker, from_date, end_date)

    return FinnHubOutput(close=response["close"], open=response["open"], high=response["high"], low=response["low"], volumn=response["volumn"], api_status=response["api_status"], time=response["time"])
