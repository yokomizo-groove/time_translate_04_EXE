from io import BytesIO
import streamlit as st

import io
import pandas as pd
import math

def to_csv_fast(final_array, headers):

    output = io.StringIO()

    st.write("Making download file with to_csv_fast")

    # ヘッダー
    output.write(",".join(headers) + "\n")

    for row in final_array:

        row_out = []

        for v in row:

            # NaN / None → 空白
            if v is None or (isinstance(v, float) and math.isnan(v)):
                row_out.append("")

            else:
                s = str(v)

                # CSV安全処理（カンマ・改行）
                if "," in s or "\n" in s or '"' in s:
                    s = '"' + s.replace('"', '""') + '"'

                row_out.append(s)

        output.write(",".join(row_out) + "\n")

    return output.getvalue().encode("utf-8-sig")


def download_file(df):

    st.write("Making download file ...")    
    
    output = BytesIO()
    df.to_excel(output, index=False, engine="xlsxwriter")
    output.seek(0)
    return output

def to_excel_xlsxwriter(df):
    output = io.BytesIO()

    # xlsxwriter をエンジンとして使う
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # writer.save() は不要（with が自動でやる）

    return output.getvalue()

def to_excel_fast_numpy_old(final_array, headers):
    output = io.BytesIO()
    import xlsxwriter

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Sheet1")

    # ヘッダー書き込み
    for col, name in enumerate(headers):
        worksheet.write(0, col, name)

    # データ書き込み（NumPy 配列を直接書く）
    rows, cols = final_array.shape
    for r in range(rows):
        for c in range(cols):
            worksheet.write(r + 1, c, final_array[r, c])

    workbook.close()
    return output.getvalue()

def to_excel_fast_numpy(final_array, headers):
    output = io.BytesIO()
    import xlsxwriter

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Sheet1")

    # ★ ヘッダーを一発で書く（write_row）
    worksheet.write_row(0, 0, headers)

    rows, cols = final_array.shape

    # ★ NumPy → list に変換して write_row で一気に書く
    for r in range(rows):
        worksheet.write_row(r + 1, 0, final_array[r].tolist())

    workbook.close()
    return output.getvalue()







