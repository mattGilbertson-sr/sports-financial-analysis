from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_market_analysis_data(workbook: Workbook):
    sheet_name = "Market Analysis - Singles"
    targeted_tables = [
        ("Market Analysis - Singles", "Market"),
    ]

    df_dict = get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )

    dict_key = list(df_dict.keys())[0]

    total_match = df_dict[dict_key]["Total T/O"].sum()

    df_dict[dict_key]["Match %"] = df_dict[dict_key]["Total T/O"] / total_match

    return df_dict
