import pandas as pd
import numpy as np
import re

pattern = re.compile(r'^(\d{1,2})[:\'](\d{1,2})(?::\d{1,2})?$')



def convert_time_series(series):
    s = series.fillna("").astype(str).str.strip()
    hm = s.str.extract(pattern)
    h = pd.to_numeric(hm[0], errors='coerce')
    m = pd.to_numeric(hm[1], errors='coerce')
    return (h * 60 + m).fillna(0).astype("int32")

def time_to_minutes(v):

    if v == "" or pd.isna(v):
        return 0

    if isinstance(v, str):
        v = v.strip()

    parts = v.split(":")

    if len(parts) < 2:
        return 0

    h = int(parts[0])
    m = int(parts[1])

    return h * 60 + m


def time_to_number(df):

    df = df.copy()

    # 列名の " を除去
    df.columns = df.columns.str.strip().str.replace('"', '', regex=False)



    # データ内の " を高速除去
    df = df.replace('"', '', regex=True)

    rows = len(df)

    # ★150列固定配列
    #final_array = np.zeros((rows, 150), dtype=object)
    final_array = np.full((rows, 150), "", dtype=object)
    
    # 元データをコピー
    original = df.to_numpy(dtype=object)
    final_array[:, :original.shape[1]] = original

    # 列名 → index
    col_index = {name: i for i, name in enumerate(df.columns)}

    mapping = {
        99: "法定内超勤時間",
        100: "早出残業時間",
        101: "普通残業時間",
        102: "実労働時間",
        103: "所定内深夜時間",
        104: "所定外深夜時間",
        106: "所定外勤務時間",
        107: "休日深夜時間",
        108: "乖離時間(開始)",
        109: "乖離時間(終了)",
        110: "年休換算時間",
        111: "調休換算時間",
        112: "不就業１時間",
        113: "所定内労働時間",
        114: "休憩時間",
        115: "特休勤務時間",
        116: "公休勤務時間",
        121: "出勤打刻",
        122: "退勤打刻",
        123: "始業時刻",
        124: "終業時刻",
    }

    converted_cache = {}

    for excel_col, col_name in mapping.items():

        if col_name in col_index:

            converted = convert_time_series(df[col_name])

            final_array[:, excel_col - 1] = converted.values

            converted_cache[col_name] = converted

    # 深夜時間計
    if "所定内深夜時間" in converted_cache and "所定外深夜時間" in converted_cache:

        total = (
            converted_cache["所定内深夜時間"]
            + converted_cache["所定外深夜時間"]
        )

        final_array[:, 105 - 1] = total.values

    # ヘッダー作成
    headers = list(df.columns)

    if len(headers) < 150:
        headers.extend([""] * (150 - len(headers)))

    for excel_col, col_name in mapping.items():
        headers[excel_col - 1] = col_name + "-t"

    headers[105 - 1] = "深夜時間計-t"

 


    return final_array, headers