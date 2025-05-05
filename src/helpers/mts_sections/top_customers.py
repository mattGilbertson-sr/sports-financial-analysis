from openpyxl import Workbook
import typing as t
import pandas as pd

from helpers.excel import get_sheet_data


def get_top_customers_data(workbook: Workbook) -> t.Dict[str, pd.DataFrame]:
    sheet_name = "Top Customers"
    targeted_tables = [
        # Top 1
        ("Top Customer by Turnover", "First Bet (UTC)"),
        ("Top Customer by Turnover - Market Data", "Bet Time (UTC)"),
        # Top 2
        ("Second Customer by Turnover", "First Bet (UTC)"),
        ("Second Customer by Turnover - Market Data", "Bet Time (UTC)"),
        # Top 3
        ("Third Customer by Turnover", "First Bet (UTC)"),
        ("Third Customer by Turnover - Market Data", "Bet Time (UTC)"),
        # Top 4
        ("Fourth Customer by Turnover", "First Bet (UTC)"),
        ("Fourth Customer by Turnover - Market Data", "Bet Time (UTC)"),
        # Top 5
        ("Fifth Customer by Turnover", "First Bet (UTC)"),
        ("Fifth Customer by Turnover - Market Data", "Bet Time (UTC)"),
    ]

    return get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )
