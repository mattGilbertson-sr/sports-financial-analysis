from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_market_summary_data(workbook: Workbook):
    sheet_name = "Market Summary - Singles"
    targeted_tables = [
        ("Market Summary - Singles", "Market"),
    ]

    return get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )
