# -*- coding: utf-8 -*-
from __future__ import annotations
import datetime

import streamlit as st


def main():
    st.title("Shelby's Gamble System")
    st.markdown("__Tích cực quay tay, vận may sẽ tới__")

    with st.sidebar:
        st.selectbox("Hôm nay xem con hàng nào:", ["AAPL", "TSLA", "VIC"])
        st.date_input("Ngày bắt đầu", datetime.date(2022, 1, 1))
        st.date_input("Ngày kết thúc")
        st.button("Lấy số đề về")


if __name__ == "__main__":
    main()
