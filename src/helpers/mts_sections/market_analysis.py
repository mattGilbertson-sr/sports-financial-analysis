from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_market_analysis_data(workbook: Workbook):
    sheet_name = "Market Analysis - Singles"
    targeted_tables = [
        ("Market Analysis - Singles", "Market"),
    ]

    return get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )
