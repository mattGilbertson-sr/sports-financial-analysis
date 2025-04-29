from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_ccf_category_summary_data(workbook: Workbook):
    sheet_name = "CCF Category Summary - Singles"
    targeted_tables = [
        ("undefined", "CCF Category"),
    ]

    return get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )
