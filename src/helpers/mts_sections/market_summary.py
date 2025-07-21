from openpyxl import Workbook
import typing as t
import pandas as pd

from helpers.excel import get_sheet_data
from helpers.market_percentage import get_market_dicts_by_period


def get_market_summary_data(
    workbook: Workbook, total_match_turnover: float
) -> t.Dict[str, pd.DataFrame]:
    sheet_name = "Market Summary - Singles"
    targeted_tables = [
        ("Market Summary - Singles", "Market"),
    ]

    df_dict = get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )

    df_dict_items = list(df_dict.items())

    for key, df in df_dict_items:
        df_dicts_by_period = get_market_dicts_by_period(key, df)

        df_dict = {**df_dict, **df_dicts_by_period}

    for df in df_dict.values():
        df["Match %"] = df["Total T/O"] / total_match_turnover

    return df_dict
