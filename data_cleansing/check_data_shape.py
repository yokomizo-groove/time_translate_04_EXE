import streamlit as st
import pandas as pd

def check_header(df1, df2):
 
    if list(df1.columns) != list(df2.columns):
        st.error("CSVのヘッダーが一致していません")
        st.stop()
    else:
        st.write("CSVのヘッダーは一致しました")


def check_row_structure(df, file):

    rows_count = len(df)

    if rows_count % 2 != 0:
        st.error(f"データ構造エラー：{file.name} で1日2行になっていない日があります")
        st.write("rows_count{rows_count} ")
        st.stop()
    else:
        st.success(f"{file.name} のデータはすべて1日2行構造です")
  

def check_date_continuity(df1, df2):

    date_col = "日付"

    df = pd.concat([df1, df2])

    df[date_col] = pd.to_datetime(df[date_col], format="%Y%m%d")

    dates = sorted(df[date_col].unique())

    for i in range(len(dates) - 1):

        if (dates[i+1] - dates[i]).days != 1:

            st.error(f"日付が連続していません: {dates[i]} → {dates[i+1]}")
            st.stop()



