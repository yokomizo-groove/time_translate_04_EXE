import streamlit as st
import os
import io
import pandas as pd
import time

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from file_system.load_data_files import load_csv_files
from file_system.export_file import to_excel_xlsxwriter, to_excel_fast_numpy, to_csv_fast

from data_cleansing.check_data_shape import check_header, check_row_structure, check_date_continuity
from data_cleansing.merge_and_sort import merge_and_sort
from data_cleansing.time_to_number import time_to_number

from basic_check.basic_check import run_basic_checks, results_to_dataframe

from config.org_master import load_org_master, get_org_info, convert_department




# ★ 高速 xlsxwriter 版 Excel 変換関数
#def to_excel_xlsxwriter(df):
#    output = io.BytesIO()
    
#    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#        df.to_excel(writer, index=False, sheet_name='Sheet1')
#    return output.getvalue()

    

def main():
 
    st.title("勤怠データチェックアプリ")

    df1, df2, file1, file2 = load_csv_files()
    
    check_header(df1, df2)
    check_date_continuity(df1, df2)
    check_row_structure(df1, file1)
    check_row_structure(df2, file2)

    st.write("CSV1")
    st.dataframe(df1)

    st.write("CSV2")
    st.dataframe(df2)
    
    st.write("DataFrame化しました")

    base_df = merge_and_sort(df1, df2)
    st.write("Base_csv_data")
    st.dataframe(base_df)
    st.write("Base_dfをDataFrame化しました")
    # st.stop()


    # ★ タイマー開始
    start = time.time()

    st.write("Translating time to numerics ...")
    final_array, headers = time_to_number(base_df)
    st.write("時間変換処理完了（-t 列追加）")
    # st.write(headers)
    # st.stop()

    
    # ③ 基本チェック実行
    results = run_basic_checks(final_array, headers)
    st.write(f"チェック件数：{len(results)} 件")
    # ④ DataFrame に変換
    df_out = results_to_dataframe(results, headers)

    # ⑤ ダウンロードボタン
    csv_bytes = df_out.to_csv(index=False, encoding="cp932").encode("cp932")


    st.download_button(
        label="チェック結果をCSVでダウンロード",
        data=csv_bytes,
        file_name="check_results.csv",
        mime="text/csv"
    )

    st.write("処理完了！")

  
    org_dict = load_org_master()
    st.success("Load org_master")
    org_order, org_name = get_org_info(11, org_dict)
    st.write(org_order, org_name)

    csv_bytes = to_csv_fast(final_array, headers)

    st.download_button(
        label="時刻→数値化後のCSVダウンロード",
        data=csv_bytes,
        file_name="temp_output.csv",
        mime="text/csv"
    )




      
        
    # ★ タイマー終了
    end = time.time() 
    elapsed = end - start

    # ★ 結果表示
    st.info(f"処理時間: {elapsed:.2f} 秒")
        
 



if __name__ == "__main__":
    main()
