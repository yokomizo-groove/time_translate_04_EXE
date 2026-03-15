import streamlit as st
import pandas as pd
   
   
def import_files():

    st.title("勤怠データチェックアプリ")

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

    st.success("CSV読み込み完了")

    st.write("CSV1")
    st.dataframe(df1)

    st.write("CSV2")
    st.dataframe(df2)
    
    st.stop()