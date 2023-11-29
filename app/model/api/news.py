# -*- coding: utf-8 -*-
from __future__ import annotations
from fastapi import FastAPI

from functools import lru_cache

import logging
from newspaper import Article

from .base import BaseFinanceAPI

MODULE_NAME = "Newspaper3k_API"
logger = logging.getLogger(MODULE_NAME)


class NewsAPI(BaseFinanceAPI):
    def __init__(self):
        self.article = None

    @lru_cache
    def connect_api(self):
        return

    def pull_data(self, url):
        self.article = Article(url)
        self.article.download()
        self.article.parse()
        logger.info(f"Successfully scrapping news: '{self.article.title}'.")

    def get_article_data(self):
        if self.article is None:
            return None

        article_data = {"title": self.article.title, "authors": self.article.authors, "publish_date": self.article.publish_date, "text": self.article.text}
        return article_data

    def clean_data(self):
        pass
