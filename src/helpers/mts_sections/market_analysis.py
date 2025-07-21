import pandas as pd
import typing as t
from openpyxl import Workbook

from helpers.excel import get_sheet_data
from helpers.market_percentage import get_market_dicts_by_period, get_market_percentage


def get_market_analysis_data(
    workbook: Workbook,
    market_summary_data: t.Dict[str, pd.DataFrame],
    total_match_turnover: float,
) -> t.Dict[str, pd.DataFrame]:
    sheet_name = "Market Analysis - Singles"
    targeted_tables = [
        ("Market Analysis - Singles", "Market"),
    ]

    df_dict = get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )

    df_dict_items = list(df_dict.items())

    for key, df in df_dict_items:
        df_dicts_by_period = get_market_dicts_by_period(key, df)

        df_dict = {**df_dict, **df_dicts_by_period}

    for df in df_dict.values():
        if not len(df):
            continue

        df["Match %"] = df["Total T/O"] / total_match_turnover
        df["Market %"] = df.apply(
            lambda x: get_market_percentage(x, market_summary_data), axis=1
        )

    return df_dict
