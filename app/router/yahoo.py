# -*- coding: utf-8 -*-
from __future__ import annotations

import logging

from constant import Message
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from helpers.utility import Utility
from model.api.yahoo import YahooFinanceAPI
from model.data.finance_api import FinanceAPIOutput

MODULE_NAME = "Yahoo"

unblock = Utility.unblock_custom(MODULE_NAME, max_workers=7)

router = APIRouter(prefix="/api/shelby-backend", tags=["Yahoo"])
logger = logging.getLogger(MODULE_NAME)

yahoo = YahooFinanceAPI()


@router.post(
    "/yahoo/pull-data",
    response_model=FinanceAPIOutput,
    responses={
        401: {"model": Message},
        500: {"model": Message},
    },
)
async def pulling_data(
    ticker: str = Form(..., description="Name of the ticker to pull data"),
):
    try:
        response = await unblock(yahoo.pull_data, ticker)

        return FinanceAPIOutput(close=response["Close"], open=response["Open"], high=response["High"], low=response["Low"], volumn=response["Volume"], date=response["Date"])

    except Exception as error:
        logger.error(Utility.format_exception(error))
        return JSONResponse(status_code=500, content={"message": str(error)})
