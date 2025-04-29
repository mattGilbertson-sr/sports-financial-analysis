from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_customer_summary_data(workbook: Workbook):
    sheet_name = "Customer Summary - Singles"
    targeted_tables = [
        ("Top 10 Customers by Accepted Turnover", "Customer"),
        ("Top 10 Customers by Rejected Turnover", "Customer"),
    ]

    return get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )
