from __future__ import annotations
from fastapi import FastAPI
import json
from newsplease import NewsPlease

from newspaper import Article

class NewsAPI:
    def __init__(self, url):
        self.url = url
        self.article = None

    def scrape_article(self):
        self.article = Article(self.url)
        self.article.download()
        self.article.parse()

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