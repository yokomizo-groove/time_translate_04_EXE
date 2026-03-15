import pandas as pd
import os


def main():
    
    OrgArray = load_org_master()

    print(OrgArray.head())

    base_code = 11

    org_code, org_name = convert_department(base_code, OrgArray)

    print(org_code, org_name)

def load_org_master():

    if os.path.exists("箇所マスタ.xlsx"):
        OrgArray = pd.read_excel("箇所マスタ.xlsx", header=6)

    elif os.path.exists("箇所マスタ.csv"):
        OrgArray = pd.read_csv("箇所マスタ.csv", header=6, encoding="utf-8")

    else:
        raise FileNotFoundError("箇所マスタが見つかりません")

    return OrgArray





def convert_department(code, OrgArray):

    row = OrgArray[OrgArray["e-works部門コード"] == code]

    if len(row) == 0:
        return None

    return row.iloc[0]["順序"], row.iloc[0]["部門（上位）"]

    print (row.iloc[0]["順序"], row.iloc[0]["部門（上位）"])


# if __name__ == "__main__":
#     main()
