import pandas as pd
import os


def main():
    
    org_dict = load_org_master()

    # print(org_dict.head())

    base_code = 11

    org_code, org_name = get_org_info(base_code, org_dict)

    print(org_code, org_name)


def load_org_master():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    xlsx_path = os.path.join(base_dir, "箇所マスタ.xlsx")
    csv_path = os.path.join(base_dir, "箇所マスタ.csv")

    if os.path.isfile(xlsx_path):
        OrgArray = pd.read_excel(xlsx_path, header=6, dtype={"e-works部門コード": "string"})

    elif os.path.isfile(csv_path):
        OrgArray = pd.read_csv(csv_path, header=6, encoding="utf-8",
                    dtype={"e-works部門コード": "string"})

    else:
        files = os.listdir(base_dir)
        raise FileNotFoundError(
            f"箇所マスタが見つかりません\n"
            f"探した場所: {base_dir}\n"
            f"configフォルダの中身: {files}"
        )

    # OrgArray["e-works部門コード"] = OrgArray["e-works部門コード"].astype(str)

    print(OrgArray.columns)

    org_dict = dict(zip(
        OrgArray["e-works部門コード"],
        zip(OrgArray["順序"], OrgArray["部門（上位）"])
    ))

    return org_dict


def get_org_info(base_code, org_dict):

    key = str(base_code)
    org_code, org_name = org_dict.get(key, (None, None))
    return org_code, org_name

def convert_department(code, OrgArray):

    row = OrgArray[OrgArray["e-works部門コード"] == code]

    if len(row) == 0:
        return None

    return row.iloc[0]["順序"], row.iloc[0]["部門（上位）"]

    print (row.iloc[0]["順序"], row.iloc[0]["部門（上位）"])


# if __name__ == "__main__":
#     main()
