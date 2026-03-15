
import pandas as pd
import streamlit as st

def merge_and_sort(df1, df2):

    df = pd.concat([df1, df2], ignore_index=True)

    df = df.sort_values(
        by=["従業員番号", "日付"],
        kind="stable"
    )

    st.success("二つのファイルを結合しソートしました")

    return df