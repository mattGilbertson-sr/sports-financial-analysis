from openpyxl import Workbook
import typing as t
import pandas as pd

from helpers.excel import get_sheet_data


def get_score_summary_data(
    workbook: Workbook, total_match_turnover: float
) -> t.Dict[str, pd.DataFrame]:
    sheet_name = "Score Summary - Singles"
    targeted_tables = [
        ("undefined", "Period"),
    ]

    df_dict = get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )

    for df in df_dict.values():
        df["Match %"] = df["Total T/O"] / total_match_turnover

    return df_dict
