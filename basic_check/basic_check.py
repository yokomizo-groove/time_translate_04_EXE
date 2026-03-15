import pandas as pd
from basic_check.columns import build_col_to_index


def run_basic_checks(final_array, headers):
    col_to_index = build_col_to_index(headers)

    # def get(row, name):
    #     return row[col_to_index[name]]

    def get(row, name):
        v = row[col_to_index[name]]
        if pd.isna(v) or v == "" or str(v) == "NaT":
            return 0
        try:
            return int(v)
        except:
            return 0


    results = []

    for i, row in enumerate(final_array):

        # --- Part1 ---
        check_0101_0701(row, i, results, get)
        check_0102_0702(row, i, results, get)
        check_0103_0104(row, i, results, get)
        check_0106(row, i, results, get)
        check_0107(row, i, results, get)
        check_0108(row, i, results, get)
        check_0109_1(row, i, results, get)
        check_0109_2(row, i, results, get)
        check_0110(row, i, results, get)
        check_0201(row, i, results, get)

        # --- Part2 ---
        check_0202_0203(row, i, results, get)
        check_0203_1(row, i, results, get)
        check_0203_2(row, i, results, get)
        check_0203_3(row, i, results, get)
        check_0204(row, i, results, get)
        check_0205_1(row, i, results, get)
        check_0205(row, i, results, get)
        check_0206_1(row, i, results, get)
        check_0206_2(row, i, results, get)
        check_0704(row, i, results, get)
        check_0207(row, i, results, get)
        check_0208(row, i, results, get)
        check_0209(row, i, results, get)
        check_0210(row, i, results, get)

        # --- Part3 ---
        check_0301_0302(row, i, results, get)
        check_0303_0304(row, i, results, get)
        check_0305_0306(row, i, results, get)
        check_0307(row, i, results, get)
        check_0308(row, i, results, get)
        check_0401_1(row, i, results, get)
        check_0401_2(row, i, results, get, final_array)
        check_0402(row, i, results, get)
        check_0403(row, i, results, get)
        check_0403_2(row, i, results, get)
        check_0703(row, i, results, get)  # 無効化されているが構造上残す

        # ← 今後の追加チェックもここに書けばOK

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


# ①⑥ 実働48時
def check_0106(row, i, results, get):
    if get(row, "実労働時間") == "48'00":
        results.append({
            "エラー名": "①⑥実働48時",
            "行番号": i,
            "元データ": row.copy()
        })


# ①⑦ 終業48時
def check_0107(row, i, results, get):
    if get(row, "終業時刻") == 2880:  # 48h * 60min
        results.append({
            "エラー名": "①⑦終業48時",
            "行番号": i,
            "元データ": row.copy()
        })


# ①⑧ 所定外0740
def check_0108(row, i, results, get):
    if get(row, "所定外勤務時間-t") >= 460:
        results.append({
            "エラー名": "①⑧所定外0740",
            "行番号": i,
            "元データ": row.copy()
        })


# ①⑨① 深夜7H以上
def check_0109_1(row, i, results, get):
    if get(row, "深夜時間計-t") >= 420:
        results.append({
            "エラー名": "①⑨①深夜7H以上",
            "行番号": i,
            "元データ": row.copy()
        })


# ①⑨② 休日深夜5H以上
def check_0109_2(row, i, results, get):
    if get(row, "休日深夜時間-t") >= 300:
        results.append({
            "エラー名": "①⑨②休日深夜5H以上",
            "行番号": i,
            "元データ": row.copy()
        })


# ①⑩ 深夜調整プラス
def check_0110(row, i, results, get):
    val = get(row, "深夜時間調整")
    if val != "" and not str(val).startswith("-") and get(row, "備考理由") == "":
        results.append({
            "エラー名": "①⑩深夜時間調整プラス",
            "行番号": i,
            "元データ": row.copy()
        })


# ②① 調休換算マイナス
def check_0201(row, i, results, get):
    if (
        str(get(row, "調休換算時間")).startswith("-") and
        get(row, "遅刻早退区分") == "" and
        get(row, "遅刻早退理由") == "" and
        get(row, "所属") != "地下鉄Ｇ"
    ):
        results.append({
            "エラー名": "②①調休換算マイナス",
            "行番号": i,
            "元データ": row.copy()
        })


# ②②②③：休出時刻なし / 半休年休換算なし
def check_0202_0203(row, i, results, get):

    # ②②休出時刻なし
    if get(row, "勤休区分") == "休出":
        if get(row, "始業時刻") == "" or get(row, "終業時刻") == "":
            results.append({
                "エラー名": "②②休出時刻なし",
                "行番号": i,
                "元データ": row.copy()
            })

    # ②③半休年休換算なし
    elif get(row, "勤休区分") in ("年PM", "年AM"):
        if get(row, "年休換算時間-t") == "":
            results.append({
                "エラー名": "②③半休年休換算なし",
                "行番号": i,
                "元データ": row.copy()
            })


# ②③① 本社半休400
def check_0203_1(row, i, results, get):
    if (
        get(row, "勤務パターン") == "日勤8H" and
        get(row, "休憩時間") == "03'30" and
        get(row, "年休換算時間-t") == "04'00"
    ):
        results.append({
            "エラー名": "②③①本社半休400",
            "行番号": i,
            "元データ": row.copy()
        })


# ②③② 年休備考理由なし
def check_0203_2(row, i, results, get):
    if get(row, "勤休区分") in ("年休", "年PM", "年AM"):
        if get(row, "備考理由") == "":
            results.append({
                "エラー名": "②③②年休備考理由なし",
                "行番号": i,
                "元データ": row.copy()
            })


# ②③③ 欠勤備考理由なし
def check_0203_3(row, i, results, get):
    if get(row, "勤休区分") == "欠勤":
        if get(row, "備考理由") == "":
            results.append({
                "エラー名": "②③③欠勤備考理由なし",
                "行番号": i,
                "元データ": row.copy()
            })


# ②④ 年休48時
def check_0204(row, i, results, get):
    if get(row, "勤休区分") in ("年PM", "年AM", "年休"):
        if get(row, "勤務パターン") == "-":
            results.append({
                "エラー名": "②④年休48時",
                "行番号": i,
                "元データ": row.copy()
            })


# ②⑤① 年休等勤務パターンなし
def check_0205_1(row, i, results, get):
    if get(row, "勤休区分") not in ("非番", "休出", "不在", ""):
        if get(row, "勤務パターン") in ("", "-"):
            results.append({
                "エラー名": "②⑤①年休等勤務パターンなし",
                "行番号": i,
                "元データ": row.copy()
            })


# ②⑤ 勤務パターン空白
def check_0205(row, i, results, get):
    if get(row, "勤休区分") not in ("非番", "忌無", "", "不在"):
        if get(row, "勤務パターン") == "":
            results.append({
                "エラー名": "②⑤勤務パターン空白",
                "行番号": i,
                "元データ": row.copy()
            })


# ②⑥① 遅刻早退理由なし
def check_0206_1(row, i, results, get):

    flag = 0

    # 終業時刻の安全な数値化
    raw_end = get(row, "終業時刻")
    try:
        end_time = int(raw_end)
    except:
        end_time = 0

    # 24:00 を超える場合の補正
    if end_time > 1440:
        end_time -= 1440

    # 遅刻早退フラグ判定
    if get(row, "不就業１区分") in ("遅刻", "早退"):
        flag = 1

    elif get(row, "出勤打刻") - get(row, "始業時刻") > 0:
        flag = 1

    elif get(row, "退勤打刻") - end_time < 0 and get(row, "退勤時刻") != 0:
        flag = 1

    # 理由なし
    if flag == 1 and get(row, "備考理由") == "":
        results.append({
            "エラー名": "②⑥①遅刻早退理由なし",
            "行番号": i,
            "元データ": row.copy()
        })



# ②⑥② 遅刻早退超勤あり
def check_0206_2(row, i, results, get):
    if get(row, "不就業１区分") in ("遅刻", "早退"):
        if get(row, "普通残業時間") != "":
            results.append({
                "エラー名": "②⑥②遅刻早退超勤あり",
                "行番号": i,
                "元データ": row.copy()
            })


# ⑦④ 遅刻等理由あり
def check_0704(row, i, results, get):
    if get(row, "不就業１区分") in ("遅刻", "早退"):
        if get(row, "備考理由") != "":
            results.append({
                "エラー名": "⑦④遅刻等理由あり",
                "行番号": i,
                "元データ": row.copy()
            })


# ②⑦ 休憩時間調整プラス
def check_0207(row, i, results, get):
    val = get(row, "休憩時間調整")
    if val != "" and not str(val).startswith("-") and get(row, "備考理由") == "":
        results.append({
            "エラー名": "②⑦休憩時間調整プラス",
            "行番号": i,
            "元データ": row.copy()
        })


# ②⑧ 乖離5H以上
def check_0208(row, i, results, get):
    if get(row, "乖離時間(開始)-t") >= 300 or get(row, "乖離時間(終了)-t") >= 300:
        results.append({
            "エラー名": "②⑧乖離5H以上",
            "行番号": i,
            "元データ": row.copy()
        })


# ②⑨ 調休換算半端
def check_0209(row, i, results, get):
    if str(get(row, "調休換算時間-t")).startswith("-") and (get(row, "調休換算時間-t") % 10 != 0):
        if get(row, "遅刻早退区分") not in ("遅刻", "早退"):
            results.append({
                "エラー名": "②⑨調休換算半端",
                "行番号": i,
                "元データ": row.copy()
            })


# ②⑩ 不就業時間半端
def check_0210(row, i, results, get):

    # 不就業１時間
    if get(row, "不就業１時間-t") % 10 != 0:
        if get(row, "不就業１区分") not in ("遅刻", "早退") and \
           get(row, "備考理由") != "" and get(row, "乖離理由") != "":
            results.append({
                "エラー名": "②⑩不就業時間半端",
                "行番号": i,
                "元データ": row.copy()
            })

    # 不就業２時間
    # elif get(row, "不就業２時間-t") % 10 != 0:
    #    if get(row, "遅刻早退区分") not in ("遅刻", "早退") and \
    #       get(row, "備考理由") != "" and get(row, "乖離理由") != "":
    #        results.append({
    #            "エラー名": "②⑩不就業時間半端",
    #            "行番号": i,
    #            "元データ": row.copy()
    #        })

# ③①③②：W / E のデータ入れ
def check_0301_0302(row, i, results, get):

    # ③① W
    if get(row, "実績") == "Ｗ":
        results.append({
            "エラー名": "③①W",
            "行番号": i,
            "元データ": row.copy()
        })

    # ③② E
    if get(row, "実績") == "Ｅ":
        results.append({
            "エラー名": "③②E",
            "行番号": i,
            "元データ": row.copy()
        })


# ③③③④：実働6H超休憩45未満 / 実働8H超休憩1H未満
def check_0303_0304(row, i, results, get):

    if get(row, "不就業１区分") == "":  # 遅刻早退なし

        work = get(row, "実労働時間-t")
        rest = get(row, "休憩時間-t")

        # ③③ 実働6H超休憩45未満
        if 360 < work <= 480 and rest < 45:
            results.append({
                "エラー名": "③③実働6H超休憩45未満",
                "行番号": i,
                "元データ": row.copy()
            })

        # ③④ 実働8H超休憩1H未満
        elif work > 480 and rest < 60:
            results.append({
                "エラー名": "③④実働8H超休憩1H未満",
                "行番号": i,
                "元データ": row.copy()
            })


# ③⑤③⑥：FSアル休 / PS特休
def check_0305_0306(row, i, results, get):

    # i が偶数行のときだけチェック（VBA と同じ）
    if i % 2 == 0:

        emp = get(row, "従業員区分")

        # ③⑤ FSアル休
        if emp in ("契約社員（時給）", "契約社員（日給）"):
            if get(row, "勤休区分") == "休(ア)" or get(final_array[i+1], "勤休区分") == "休(ア)":
                results.append({
                    "エラー名": "③⑤FSアル休",
                    "行番号": i,
                    "元データ": row.copy()
                })

        # ③⑥ PS特休
        elif emp == "パートタイムスタッフ":
            if get(row, "勤休区分") == "特休" or get(final_array[i+1], "勤休区分") == "特休":
                results.append({
                    "エラー名": "③⑥PS特休",
                    "行番号": i,
                    "元データ": row.copy()
                })


# ③⑦ 出勤退勤打忘
def check_0307(row, i, results, get):

    start = get(row, "出勤区分")
    end = get(row, "退勤区分")

    if start == "打忘" or end == "打忘":
        results.append({
            "エラー名": "③⑦出勤退勤打忘",
            "行番号": i,
            "元データ": row.copy()
        })


# ③⑧ 勤休区分勤務PT組み合わせ誤り
def check_0308(row, i, results, get):

    if get(row, "勤休区分") != "":

        # 休出
        if get(row, "勤休区分") == "休出" and get(row, "勤務パターン") != "-":
            results.append({
                "エラー名": "③⑧勤休区分勤務PT組み合わせ誤り",
                "行番号": i,
                "元データ": row.copy()
            })

        # その他
        elif get(row, "勤休区分") not in ("休出", ""):
            if get(row, "勤務パターン") in ("", "-"):
                results.append({
                    "エラー名": "③⑧勤休区分勤務PT組み合わせ誤り",
                    "行番号": i,
                    "元データ": row.copy()
                })


# ④①① 特殊作業手当勤務なし
def check_0401_1(row, i, results, get):

    if get(row, "特殊作業") != "":
        if get(row, "始業時刻") == "" and get(row, "終業時刻") == "" and get(row, "勤務パターン") != "非番":
            results.append({
                "エラー名": "④①①特殊作業手当勤務なし",
                "行番号": i,
                "元データ": row.copy()
            })


# ④①② 特殊作業手当複数
def check_0401_2(row, i, results, get, final_array):

    # 次の行が存在する場合のみ
    if i + 1 < len(final_array):

        if get(row, "特殊作業") != "" and get(final_array[i+1], "特殊作業") != "":
            if get(row, "日付") == get(final_array[i+1], "日付"):

                results.append({
                    "エラー名": "④①②特殊作業手当複数",
                    "行番号": i,
                    "元データ": row.copy()
                })

                # 次の行も出力
                results.append({
                    "エラー名": "④①②特殊作業手当複数",
                    "行番号": i+1,
                    "元データ": final_array[i+1].copy()
                })


# ④② 緊急呼出勤務なし
def check_0402(row, i, results, get):

    if get(row, "緊急呼出") != "":
        if get(row, "始業時刻") == "" and get(row, "終業時刻") == "":
            results.append({
                "エラー名": "④②緊急呼出勤務なし",
                "行番号": i,
                "元データ": row.copy()
            })


# ④③ 泊り、特殊作業と勤務不整合
def check_0403(row, i, results, get):

    if get(row, "泊り") != "" and get(row, "特殊作業") != "":
        if get(row, "所定内深夜時間") == "" and get(row, "所定外深夜時間") == "":
            results.append({
                "エラー名": "④③泊り、特殊作業と勤務不整合",
                "行番号": i,
                "元データ": row.copy()
            })


# ④③② 隔日交代と泊りフラグ不整合
def check_0403_2(row, i, results, get):

    if get(row, "泊り") != "" and get(row, "所定内労働時間-t") < 920:
        results.append({
            "エラー名": "④③②隔日交代と泊りフラグ不整合",
            "行番号": i,
            "元データ": row.copy()
        })


# ⑦③ 実績NotApproval（※VBAでは Exit Function で無効化）
def check_0703(row, i, results, get):
    pass  # VBA と同じく無効化


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
