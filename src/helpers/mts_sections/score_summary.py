from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_score_summary_data(workbook: Workbook):
    sheet_name = "Score Summary - Singles"
    targeted_tables = [
        ("undefined", "Period"),
    ]

    return get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )
