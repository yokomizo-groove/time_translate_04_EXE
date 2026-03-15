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

    df1 = pd.read_csv(file1, encoding="cp932")
    df2 = pd.read_csv(file2, encoding="cp932")

    if list(df1.columns) != list(df2.columns):
        st.error("CSVのヘッダーが一致していません")
        st.stop()

    check_row_structure(df1, file1)
    check_row_structure(df2, file2)

    st.success("CSV読み込み完了")

    return df1, df2

def check_data_shapes(df, file):



def check_row_structure(df, file):

    rows_count = len(df)

    if rows_count % 2 == 0:
        st.error("データ構造エラー：{file.name} で1日2行になっていない日があります")
        st.stop()
  