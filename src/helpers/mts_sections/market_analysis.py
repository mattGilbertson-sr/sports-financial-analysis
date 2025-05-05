import pandas as pd
import typing as t
from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_market_percentage(market: pd.Series, market_summary_df: pd.DataFrame) -> float:
    df_filtered = market_summary_df[market_summary_df["Market"] == market["Market"]]

    if not len(df_filtered):
        return 0

    return market["Total T/O"] / df_filtered.iloc[0]["Total T/O"]


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

    market_summary_df = market_summary_data["Market Summary - Singles"]

    for df in df_dict.values():
        df["Match %"] = df["Total T/O"] / total_match_turnover
        df["Market %"] = df.apply(
            lambda x: get_market_percentage(x, market_summary_df), axis=1
        )

    return df_dict
