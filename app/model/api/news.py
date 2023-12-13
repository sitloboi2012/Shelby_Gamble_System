# -*- coding: utf-8 -*-
from __future__ import annotations
from fastapi import FastAPI

from functools import lru_cache

import logging
import feedparser
from datetime import datetime
from urllib.parse import urlparse
import pytz
import streamlit as st
from newspaper import Article

from .base import BaseFinanceAPI

MODULE_NAME = "Newspaper3k_API"
logger = logging.getLogger(MODULE_NAME)

temp = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"
rss_urls = [
    "http://feeds.marketwatch.com/marketwatch/topstories/",
    "http://rss.cnn.com/rss/cnn_latest.rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://feeds.washingtonpost.com/rss/business?itid=lk_inline_manual_37",
    "https://feeds.washingtonpost.com/rss/world?itid=lk_inline_manual_36",
]

url_list = []


class NewsAPI(BaseFinanceAPI):
    def __init__(self):
        self.articles = []

    @lru_cache
    def connect_api(self):
        return

    def pull_data(self):
        url_list = extract_and_save_urls()
        for url in url_list:
            article = Article(url)
            article.download()
            article.parse()
            self.articles.append(article)
            logger.info(f"Successfully scrapping news: '{article.title}'.")

    def get_articles_data(self):
        articles_data = []
        for article in self.articles:
            article_data = {"title": article.title, "authors": article.authors, "text": article.text}
            articles_data.append(article_data)
        return articles_data

    def clean_data(self):
        pass


def extract_and_save_urls():
    current_time_zone = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(current_time_zone)

    for url in rss_urls:
        feed = feedparser.parse(url)

        unique_urls = set()

        for entry in feed.entries:
            pub_date_struct = entry.published_parsed
            url = entry.link

            parsed_url = urlparse(url)
            if not parsed_url.path or parsed_url.path == "/":
                continue

            pub_date = datetime(*pub_date_struct[:6], tzinfo=pytz.utc)

            pub_date_local = pub_date.astimezone(current_time_zone)

            time_difference = current_time - pub_date_local

            # if time_difference > timedelta(hours=48):
            #     continue

            if url in unique_urls:
                continue

            unique_urls.add(url)

            url_list.append(url)

    return url_list
