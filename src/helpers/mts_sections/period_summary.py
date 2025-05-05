from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_period_summary_data(workbook: Workbook):
    sheet_name = "Period Summary - Singles"
    targeted_tables = [
        ("undefined", "Period"),
    ]

    df_dict = get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )

    dict_key = list(df_dict.keys())[0]

    total_match = df_dict[dict_key]["Total T/O"].sum()

    df_dict[dict_key]["Match %"] = df_dict[dict_key]["Total T/O"] / total_match

    return df_dict
