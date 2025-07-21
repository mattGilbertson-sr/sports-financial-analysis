from openpyxl import Workbook
import typing as t
import pandas as pd

from helpers.excel import get_sheet_data


def get_bookmaker_summary_data(
    workbook: Workbook, total_match_turnover: float
) -> t.Dict[str, pd.DataFrame]:
    sheet_name = "Bookmaker Summary - Singles"
    targeted_tables = [
        ("Top 10 Bookmakers by Accepted Turnover", "Bookmaker"),
        ("Top 10 Bookmakers by Rejected Turnover", "Bookmaker"),
    ]

    df_dict = get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )

    for df in df_dict.values():
        df["Match %"] = df["Total T/O"] / total_match_turnover

    return df_dict
