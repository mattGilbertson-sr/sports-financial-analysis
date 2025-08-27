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

    # Group rows with same Market value and sum numeric columns
    for key, df in df_dict.items():
        if "Market" in df.columns and len(df) > 0:
            # Identify numeric columns (exclude Market column)
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            
            # Group by Market and sum numeric columns
            df_grouped = df.groupby("Market", as_index=False)[numeric_columns].sum().sort_values(by="Total T/O", ascending=False)   
            
            # Update the dataframe in the dictionary
            df_dict[key] = df_grouped

    df_dict_items = list(df_dict.items())

    for key, df in df_dict_items:
        df_dicts_by_period = get_market_dicts_by_period(key, df)

        df_dict = {**df_dict, **df_dicts_by_period}

    for df in df_dict.values():
        df["Match %"] = df["Total T/O"] / total_match_turnover

    return df_dict
