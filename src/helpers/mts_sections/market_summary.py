from openpyxl import Workbook
import typing as t
import pandas as pd

from helpers.excel import get_sheet_data


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
        df["Match %"] = df["Total T/O"] / total_match_turnover

    return df_dict
