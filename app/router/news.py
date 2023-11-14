# -*- coding: utf-8 -*-
from __future__ import annotations

import logging

from constant import Message
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from helpers.utility import Utility
from model.api.news import NewsAPI
from model.data.news_api import NewsArticleOutput

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
async def pulling_data(
    url: str = Form(..., description="News URL to pull data"),
):
    try:
        news_api = NewsAPI()
        news_api.pull_data(url)
        article_data = news_api.get_article_data()

        if article_data:
            output_data = NewsArticleOutput(
                title=article_data["title"],
                authors=article_data["authors"],
                # publish_date=article_data["publish_date"],
                text=article_data["text"],
            )
            return output_data
        else:
            return JSONResponse(status_code=404, content={"message": "News article not found"})

    except Exception as error:
        logger.error(Utility.format_exception(error))
        return JSONResponse(status_code=500, content={"message": str(error)})
