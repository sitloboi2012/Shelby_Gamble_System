# -*- coding: utf-8 -*-
from __future__ import annotations

import ast
import datetime

import requests
import streamlit as st

URL_FINHUB = "http://localhost:8080/api/shelby-backend/finnhub/pull-data"
URL_YAHOO = "http://localhost:8080/api/shelby-backend/yahoo/pull-data"
URL_NEWS = "http://localhost:8080/api/shelby-backend/news/pull-data"


def input_form():
    with st.form("data-form"):
        ticker = st.selectbox("Hôm nay xem con hàng nào:", ["AAPL", "TSLA"])
        from_date = st.date_input("Ngày bắt đầu", datetime.date(2022, 1, 1))
        end_date = st.date_input("Ngày kết thúc")
        export_api = st.form_submit_button("Lấy số đề về")
    return ticker, from_date, end_date, export_api


def interface():
    st.title("Shelby's Gamble System")
    st.markdown("__Tích cực quay tay, vận may sẽ tới__")

    with st.sidebar:
        ticker, from_date, end_date, export_api = input_form()

    if export_api:
        with st.spinner("Ngủ đi! Hàng đang về"):
            response_finnhub = requests.request(
                "POST",
                URL_FINHUB,
                headers={},
                data={"ticker": ticker, "from_date": from_date, "end_date": end_date},
            )

            response_yahoo = requests.request(
                "POST",
                URL_YAHOO,
                headers={},
                data={"ticker": ticker},
            )

            st.write(response_finnhub.text)
            st.dataframe(response_finnhub.text, use_container_width=True)
            st.dataframe(response_yahoo.text, use_container_width=True)

    news_scraper_section()


def news_scraper_section():
    st.sidebar.header("News Scraper")
    article_url = st.sidebar.text_input("Enter the URL of a news article:")
    scrape_button = st.sidebar.button("Scrape Article")

    if scrape_button and article_url:
        response_news = requests.post(
            URL_NEWS,
            data={"url": article_url},
            headers={},
        )

        if response_news.status_code == 200:
            news_data = ast.literal_eval(response_news.text)

            st.subheader("News Article Details")
            st.write(f"Title: {news_data['title']}")
            st.write(f"Authors: {', '.join(news_data['authors'])}")
            st.write(f"Publish Date: {news_data['publish_date']}")
            st.write(f"Article Text: {news_data['text']}")
        else:
            st.error("Failed to scrape the news article. Please check the URL.")


interface()

# LEGACY
# response_1 = FINNHUB_OBJ.pull_data(ticker, str(from_date), str(end_date))
# response_2 = YAHOO_OBJ.pull_data(ticker)  # type: ignore
# filename = f"{ticker}-{from_date}-{end_date}-{datetime.datetime.now().date()}"
# Utility.create_tmp_file(response_1, filename)  # type: ignore
# st.write("Dậy đi ông cháu ơi! Hàng về rồi")
# if export_api:
#    st.dataframe(response_1, use_container_width=True)
#    st.dataframe(response_2, use_container_width=True)
# elif export_download:
#    st.download_button("Download", json.dumps(response_1))
