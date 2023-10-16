# -*- coding: utf-8 -*-
from __future__ import annotations
import datetime

import json
import streamlit as st

from helpers.utility import Utility
from model.finnhub import FinnHubAPI

FINNHUB_OBJ = FinnHubAPI()


def input_data():
    with st.form("data-form"):
        ticker = st.selectbox("Hôm nay xem con hàng nào:", ["AAPL", "TSLA"])
        from_date = st.date_input("Ngày bắt đầu", datetime.date(2022, 1, 1))
        end_date = st.date_input("Ngày kết thúc")
        export_api = st.form_submit_button("Lấy số đề về")
        export_download = st.form_submit_button("Tải số đề về")
    return ticker, from_date, end_date, export_api, export_download


def export_data():
    pass


def interface():
    st.title("Shelby's Gamble System")
    st.markdown("__Tích cực quay tay, vận may sẽ tới__")

    with st.sidebar:
        ticker, from_date, end_date, export_api, export_download = input_data()

    if export_api:
        with st.spinner("Ngủ đi! Hàng đang về"):
            response = FINNHUB_OBJ.pull_data(ticker, str(from_date), str(end_date))
        Utility.create_tmp_file(response, f"{ticker}-{from_date}-{end_date}-{datetime.datetime.now().date()}")  # type: ignore
        st.write("Dậy đi ông cháu ơi! Hàng về rồi")
        st.dataframe(response, use_container_width=True)
    elif export_download:
        with st.spinner("Ngủ đi! Hàng đang về"):
            response = FINNHUB_OBJ.pull_data(ticker, str(from_date), str(end_date))
        st.write("Dậy đi ông cháu ơi! Hàng về rồi")
        st.download_button("Download", json.dumps(response))  # type: ignore
