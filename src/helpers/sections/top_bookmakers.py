from openpyxl import Workbook
import typing as t
import pandas as pd

from helpers.excel import get_sheet_data
from helpers.market_percentage import get_market_percentage


def get_top_bookmakers_data(
    workbook: Workbook,
    market_summary_data: t.Dict[str, pd.DataFrame],
    total_match_turnover: float,
) -> t.Dict[str, pd.DataFrame]:
    sheet_name = "Top Bookmakers - Top Markets"
    targeted_tables = [
        # Top 1
        ("Top Bookmaker by Turnover", "Market"),
        # Top 2
        ("Second Bookmaker by Turnover", "Market"),
        # Top 3
        ("Third Bookmaker by Turnover", "Market"),
    ]

    df_dict = get_sheet_data(
        workbook=workbook,
        sheet_name=sheet_name,
        target_tables=targeted_tables,
        include_full_table_name=True,
    )

    for df in df_dict.values():
        if not len(df):
            continue

        df["Match %"] = df["Total T/O"] / total_match_turnover
        df["Market %"] = df.apply(
            lambda x: get_market_percentage(x, market_summary_data), axis=1
        )

    return df_dict
