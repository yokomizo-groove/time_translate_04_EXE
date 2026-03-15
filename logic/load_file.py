import pandas as pd
import numpy as np
import os
import streamlit as st



def load_file(uploaded_file, MAX_COL=150):

    st.write("Load File ...")
    
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    uploaded_file.seek(0)

    # ===== CSV =====
    if ext == ".csv":
        raw_bytes = uploaded_file.read()

        # エンコード判定
        for enc in ["utf-8", "cp932"]:
            try:
                raw_text = raw_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            raw_text = raw_bytes.decode("utf-8", errors="replace")

        rows = [line.split(",") for line in raw_text.splitlines()]
        row_count = len(rows)

        base_array = np.empty((row_count, MAX_COL), dtype=object)
        base_array[:] = ""

        for i, cols in enumerate(rows):
            limit = min(len(cols), MAX_COL)
            base_array[i, :limit] = cols[:limit]

        header = base_array[0]
        data = base_array[1:]

        df = pd.DataFrame(data, columns=header)
        df = df.fillna("")

        # ★ 1〜5列目のどれかにデータがある行だけを残す
        key_cols = df.columns[:5]  # 1〜5列目
        valid_rows = df[key_cols].apply(lambda row: any(str(x).strip() for x in row), axis=1)
        df = df[valid_rows].reset_index(drop=True)

        return df

    # ===== Excel =====
    elif ext in [".xlsx", ".xlsm"]:
        df = pd.read_excel(uploaded_file, dtype=str).fillna("")
        df = df.astype(str)  # 時刻型 → 文字列化

        row_count = len(df)
        base_array = df.to_numpy(dtype=object)

        if base_array.shape[1] < MAX_COL:
            pad = np.empty((row_count, MAX_COL - base_array.shape[1]), dtype=object)
            pad[:] = ""
            base_array = np.hstack([base_array, pad])

            cols = list(df.columns)
        if len(cols) < MAX_COL:
            cols += [""] * (MAX_COL - len(cols))

        df = pd.DataFrame(base_array, columns=cols)
        df = df.fillna("")

        # ★ 1〜10列目のどれかにデータがある行だけを残す
        key_cols = df.columns[:10]  # 1〜10列目
        valid_rows = df[key_cols].apply(lambda row: any(str(x).strip() for x in row), axis=1)
        df = df[valid_rows].reset_index(drop=True)

        return df


    else:
        raise ValueError("Unsupported file format")




