import pandas as pd
import typing as t
from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_market_percentage(
    market: pd.Series, market_summary_data: t.Dict[str, pd.DataFrame]
) -> float:
    # Filter by period
    if "1st half" in market["Market"]:
        df_filtered = market_summary_data["Market Summary - Singles - 1H"]
    elif "2nd half" in market["Market"]:
        df_filtered = market_summary_data["Market Summary - Singles - 2H"]
    else:
        df_filtered = market_summary_data["Market Summary - Singles - FT"]

    # Filter by market
    if "handicap" in market["Market"].lower():
        df_filtered = df_filtered[
            df_filtered["Market"].str.contains("handicap", case=False, na=False)
        ]
    elif "total corners" in market["Market"].lower():
        df_filtered = df_filtered[
            df_filtered["Market"].str.contains("total corners", case=False, na=False)
        ]
    elif "total" in market["Market"].lower():
        df_filtered = df_filtered[
            df_filtered["Market"].str.contains("total", case=False, na=False)
        ]
    else:
        df_filtered = df_filtered[df_filtered["Market"] == market["Market"]]

    if not len(df_filtered):
        return 0

    return market["Total T/O"] / df_filtered["Total T/O"].sum()


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

    for df in df_dict.values():
        df["Match %"] = df["Total T/O"] / total_match_turnover
        df["Market %"] = df.apply(
            lambda x: get_market_percentage(x, market_summary_data), axis=1
        )

    return df_dict
