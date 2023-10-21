# -*- coding: utf-8 -*-
from __future__ import annotations
import datetime
import logging
import json
import streamlit as st

from helpers.utility import Utility
from model.finnhub import FinnHubAPI
from model.news import NewsAPI

MODULE_NAME = "Main"
logger = logging.getLogger(MODULE_NAME)
from model.yahoo import YahooFinanceAPI

FINNHUB_OBJ = FinnHubAPI()
YAHOO_OBJ = YahooFinanceAPI()


def input_form():
    with st.form("data-form"):
        ticker = st.selectbox("Hôm nay xem con hàng nào:", ["AAPL", "TSLA"])
        from_date = st.date_input("Ngày bắt đầu", datetime.date(2022, 1, 1))
        end_date = st.date_input("Ngày kết thúc")
        export_api = st.form_submit_button("Lấy số đề về")
        export_download = st.form_submit_button("Tải số đề về")
    return ticker, from_date, end_date, export_api, export_download


def interface():
    st.title("Shelby's Gamble System")
    st.markdown("__Tích cực quay tay, vận may sẽ tới__")

    with st.sidebar:
        ticker, from_date, end_date, export_api, export_download = input_form()

    if export_api or export_download:
        with st.spinner("Ngủ đi! Hàng đang về"):
            response_1 = FINNHUB_OBJ.pull_data(ticker, str(from_date), str(end_date))
            response_2 = YAHOO_OBJ.pull_data(ticker)  # type: ignore
        filename = f"{ticker}-{from_date}-{end_date}-{datetime.datetime.now().date()}"
        Utility.create_tmp_file(response_1, filename)  # type: ignore
        st.write("Dậy đi ông cháu ơi! Hàng về rồi")
        if export_api:
            st.dataframe(response_1, use_container_width=True)
            st.dataframe(response_2, use_container_width=True)
        elif export_download:
            st.download_button("Download", json.dumps(response_1))
            
    news_scraper_section()
            
            
            


def news_scraper_section():
    st.sidebar.header("News Scraper")

    article_url = st.sidebar.text_input("Enter the URL of a news article:")
    scrape_button = st.sidebar.button("Scrape Article")

    if scrape_button and article_url:
        news_scraper = NewsAPI(article_url)

        news_scraper.pull_data()

        article_data = news_scraper.get_article_data()

        if article_data:
            st.subheader("Article Details")
            st.write(f"Title: {article_data['title']}")
            st.write(f"Author: {article_data['authors']}")
            st.write(f"Publish Date: {article_data['publish_date']}")
            st.write(f"Article Text: {article_data['text']}")
        else:
            st.error("Failed to scrape the article. Please check the URL.")