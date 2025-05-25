import pandas as pd
import typing as t
from openpyxl import Workbook

from helpers.excel import get_sheet_data


def get_market_percentage(
    market: pd.Series,
    market_summary_data: t.Dict[str, pd.DataFrame],
    teams: t.List[str],
) -> float:
    # Filter by period
    period_market = None
    if "1st half" in market["Market"]:
        df_filtered = market_summary_data["Market Summary - Singles - 1H"]
        period_market = "1st half"
    elif "2nd half" in market["Market"]:
        df_filtered = market_summary_data["Market Summary - Singles - 2H"]
        period_market = "2nd half"
    else:
        df_filtered = market_summary_data["Market Summary - Singles - FT"]

    # Filter by market
    if "handicap" in market["Market"].lower():
        df_filtered = df_filtered[
            df_filtered["Market"].str.contains("handicap", case=False, na=False)
        ]
    elif "total" == market["Market"].lower() or (
        period_market and f"{period_market} - total" == market["Market"].lower()
    ):
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

    # Define both teams
    ft_market_data = df_dict["Market Analysis - Singles"]
    teams = ft_market_data[
        (ft_market_data["Market"] == "1x2") & (ft_market_data["Selection"] != "draw")
    ]["Selection"].tolist()
    teams = [t.lower() for t in teams]

    df_dict_items = list(df_dict.items())

    for key, df in df_dict_items:
        df_dict[f"{key} - FT"] = df[
            (~df["Market"].str.contains("1st half", case=False, na=False))
            & (~df["Market"].str.contains("2nd half", case=False, na=False))
        ]
        df_dict[f"{key} - 1H"] = df[
            df["Market"].str.contains("1st half", case=False, na=False)
        ]
        df_dict[f"{key} - 2H"] = df[
            df["Market"].str.contains("2nd half", case=False, na=False)
        ]

    for df in df_dict.values():
        if not len(df):
            continue

        df["Match %"] = df["Total T/O"] / total_match_turnover
        df["Market %"] = df.apply(
            lambda x: get_market_percentage(x, market_summary_data, teams), axis=1
        )

    return df_dict
