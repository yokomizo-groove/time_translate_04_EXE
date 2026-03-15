import streamlit as st
import pandas as pd
   
   
def load_csv_files():

    st.markdown("""
        ### CSVファイルをアップロードしてください

        1か月目と2か月目のCSVを選択してください
    """)

    file1 = st.file_uploader("1か月目CSV", type="csv")
    if file1:
        st.write("読み込んだファイル:", file1.name)

    file2 = st.file_uploader("2か月目CSV", type="csv")
    if file2:
        st.write("読み込んだファイル:", file2.name)

    if file1 is None or file2 is None:
        st.warning("CSVファイルを2つ選択してください")
        st.stop()

    # df1 = pd.read_csv(file1, encoding="cp932")
    # df2 = pd.read_csv(file2, encoding="cp932")

    df1 = pd.read_csv(file1, encoding="cp932", dtype=str, keep_default_na=False)
    df2 = pd.read_csv(file2, encoding="cp932", dtype=str, keep_default_na=False)

 
    st.success("CSV読み込み完了")

    return df1, df2, file1, file2
