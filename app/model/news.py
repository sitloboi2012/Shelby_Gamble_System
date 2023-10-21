from __future__ import annotations
from fastapi import FastAPI
import json

from functools import lru_cache

import logging
from newspaper import Article

from .base import BaseFinanceAPI

MODULE_NAME = "Newspaper3k_API"
logger = logging.getLogger(MODULE_NAME)

    
class NewsAPI(BaseFinanceAPI):
    def __init__(self, url):
        self.url = url
        self.article = None
        
    @lru_cache
    def connect_api(self):
        return
    
    def pull_data(self):
        self.article = Article(self.url)
        self.article.download()
        self.article.parse()
        logger.info(f"Successfully pulling {self.article.title}.")
        
        
    def get_article_data(self):
        if self.article is None:
            return None

        article_data = {
            "title": self.article.title,
            "authors": self.article.authors,
            "publish_date": self.article.publish_date,
            "text": self.article.text
        }
        return article_data
    
    def clean_data(self):
        pass