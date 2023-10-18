# -*- coding: utf-8 -*-
from __future__ import annotations

import ast
import datetime

import requests
import streamlit as st

URL_FINHUB = "http://localhost:8080/api/shelby-backend/finnhub/pull-data"
URL_YAHOO = "http://localhost:8080/api/shelby-backend/yahoo/pull-data"


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

            st.dataframe(ast.literal_eval(response_finnhub.text), use_container_width=True)
            st.dataframe(ast.literal_eval(response_yahoo.text), use_container_width=True)


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
