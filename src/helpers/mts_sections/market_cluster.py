from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_market_cluster_data(workbook: Workbook):
    sheet_name = "Market Cluster - Singles"
    targeted_tables = [
        ("Market Cluster - Singles - Accepted/Rejected", "Market"),
    ]

    return get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )
