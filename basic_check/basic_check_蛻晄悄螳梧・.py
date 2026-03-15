import pandas as pd
from basic_check.columns import build_col_to_index


def run_basic_checks(final_array, headers):
    # headers から index 辞書を作成
    col_to_index = build_col_to_index(headers)

    # 列名アクセス関数（ローカルに閉じる）
    def get(row, name):
        return row[col_to_index[name]]

    results = []

    for i, row in enumerate(final_array):
        check_0101_0701(row, i, results, get)
        check_0102_0702(row, i, results, get)
        check_0103_0104(row, i, results, get)

        # ← ここに今後 40 個追加していく

    return results


# ①①⑦①：始業乖離 / 始業理由あり
def check_0101_0701(row, i, results, get):
    if get(row, "乖離時間(開始)-t") >= 30:

        if (
            get(row, "出勤区分") == "" and
            get(row, "備考理由") == "" and
            get(row, "乖離理由") == ""
        ):
            error_name = "①①始業乖離"
        else:
            error_name = "⑦①始業理由あり"

        results.append({
            "エラー名": error_name,
            "行番号": i,
            "元データ": row.copy()
        })


# ①②⑦②：終業乖離 / 終業理由あり
def check_0102_0702(row, i, results, get):
    if get(row, "乖離時間(終了)-t") >= 30:

        if (
            get(row, "退勤区分") == "" and
            get(row, "備考理由") == "" and
            get(row, "乖離理由") == ""
        ):
            error_name = "①②終業乖離"
        else:
            error_name = "⑦②終業理由あり"

        results.append({
            "エラー名": error_name,
            "行番号": i,
            "元データ": row.copy()
        })


# ①④勤務パターン不整合
def check_0103_0104(row, i, results, get):

    if (
        get(row, "休日区分") != "" and
        get(row, "勤休区分") != "不在" and
        get(row, "勤務パターン") not in ("", "-")
    ):
        results.append({
            "エラー名": "①④勤務パターン不整合",
            "行番号": i,
            "元データ": row.copy()
        })


# 結果を DataFrame に変換（headers を使う）
def results_to_dataframe(results, headers):
    rows = []

    for item in results:
        base = {
            "エラー名": item["エラー名"],
            "行番号": item["行番号"],
        }

        # final_array の 155 列を展開
        row_data = {col: val for col, val in zip(headers, item["元データ"])}

        base.update(row_data)
        rows.append(base)

    return pd.DataFrame(rows)
