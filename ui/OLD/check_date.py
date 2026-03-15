import streamlit as st
import pandas as pd

def check_date_continuity(df1, df2):

    date_col = "日付"

    df = pd.concat([df1, df2])

    df[date_col] = pd.to_datetime(df[date_col], format="%Y%m%d")

    dates = sorted(df[date_col].unique())

    for i in range(len(dates) - 1):

        if (dates[i+1] - dates[i]).days != 1:

            st.error(f"日付が連続していません: {dates[i]} → {dates[i+1]}")
            st.stop()
