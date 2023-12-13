# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import boto3
import streamlit as st
import json
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile

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
async def pulling_data():
    try:
        news_api = NewsAPI()
        news_api.pull_data()
        articles_data = news_api.get_articles_data()

        if articles_data:
            json_data = json.dumps(articles_data, indent=2)

            # Save JSON data to a temporary file
            with NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_file:
                temp_file.write(json_data)
                temp_file_path = temp_file.name

            # Return the JSON file as a response
            return FileResponse(temp_file_path, filename="news_data.json", media_type="application/json")
            # output_data = [
            #     {
            #         "title": article["title"],
            #         "authors": article["authors"],
            #         "text": article["text"],
            #     }
            #     for article in articles_data
            # ]

            # s3 = boto3.client('s3', aws_access_key_id="AKIARBS75YKKQAX4Z55N", aws_secret_access_key="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", region_name='ap-southeast-1')
            # bucket_name = 'shelby-data-store'
            # for idx, article_data in enumerate(articles_data):
            #     file_name = f"article_{idx + 1}.json"
            #     s3_key = f"news_articles/{file_name}"

            #     # Save article data to JSON file
            #     with open(file_name, 'w') as json_file:
            #         json.dump(article_data, json_file)

            #     # Upload the JSON file to S3
            #     s3.upload_file(file_name, bucket_name, s3_key)
            # with open("articles_data.json", "w") as json_file:
            #     json.dump(output_data, json_file)

            # return output_data
        else:
            return JSONResponse(status_code=404, content={"message": "No news articles found"})

    except Exception as error:
        logger.error(Utility.format_exception(error))
        return JSONResponse(status_code=500, content={"message": str(error)})
