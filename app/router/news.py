# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import boto3
import streamlit as st
from fastapi.responses import FileResponse
import pandas as pd

from constant import Message
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from helpers.utility import Utility
from model.api.news import NewsAPI
from model.data.news_api import NewsArticleOutput
from model.data_preprocessing.news_data_preprocessing import text_preparation

MODULE_NAME = "News"

unblock = Utility.unblock_custom(MODULE_NAME, max_workers=7)

router = APIRouter(prefix="/api/shelby-backend", tags=["News"])
logger = logging.getLogger(MODULE_NAME)


@router.post(
    "/news/pull-data",
    response_model=NewsArticleOutput,
    responses={
        401: {"model": Message},
        500: {"model": Message},
    },
)
async def pulling_data():
    try:
        news_api = NewsAPI()
        news_api.pull_data()
        articles_data = news_api.get_articles_data()

        if articles_data:
            df = pd.DataFrame(articles_data)
            clean_df = text_preparation(df)

            return JSONResponse(content=clean_df.to_json(orient="records"), media_type="application/json")

        else:
            return JSONResponse(status_code=404, content={"message": "No news articles found"})

    except Exception as error:
        logger.error(Utility.format_exception(error))
        return JSONResponse(status_code=500, content={"message": str(error)})
