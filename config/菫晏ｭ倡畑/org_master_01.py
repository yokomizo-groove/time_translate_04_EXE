import pandas as pd
import os


def main():
    
    org_dict = load_org_master()

    # print(org_dict.head())

    base_code = 11

    org_code, org_name = get_org_info(base_code, org_dict)

    print(org_code, org_name)

def load_org_master():

    if os.path.exists("箇所マスタ.xlsx"):
        OrgArray = pd.read_excel("箇所マスタ.xlsx", header=6)

    elif os.path.exists("箇所マスタ.csv"):
        OrgArray = pd.read_csv("箇所マスタ.csv", header=6, encoding="utf-8")

    else:
        raise FileNotFoundError("箇所マスタが見つかりません")

    # return OrgArray

    org_dict = dict(zip(
    OrgArray["e-works部門コード"],
    zip(OrgArray["順序"], OrgArray["部門（上位）"])
    ))

    return org_dict

def get_org_info(code, org_dict):

    org_code, org_name = org_dict.get(code, (None, None))

    return org_code, org_name

def convert_department(code, OrgArray):

    row = OrgArray[OrgArray["e-works部門コード"] == code]

    if len(row) == 0:
        return None

    return row.iloc[0]["順序"], row.iloc[0]["部門（上位）"]

    print (row.iloc[0]["順序"], row.iloc[0]["部門（上位）"])


if __name__ == "__main__":
    main()
