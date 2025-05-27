from openpyxl import Workbook
import typing as t
import pandas as pd

from helpers.excel import get_sheet_data


def get_customer_key_splitted(key: str) -> t.Tuple[str, str]:
    if "Bookmaker" not in key:
        return key

    bookmaker_index = key.index("Bookmaker")

    return key[:bookmaker_index], key[bookmaker_index:]


def get_top_customers_data(workbook: Workbook) -> t.Dict[str, pd.DataFrame]:
    sheet_name = "Top Customers"
    targeted_tables = [
        # Top 1
        ("Top Customer by Turnover", "First Bet (UTC)"),
        ("Top Customer by Turnover - Market Data", "Bet Time (UTC)"),
        # Top 2
        ("Second Customer by Turnover", "First Bet (UTC)"),
        ("Second Customer by Turnover - Market Data", "Bet Time (UTC)"),
        # Top 3
        ("Third Customer by Turnover", "First Bet (UTC)"),
        ("Third Customer by Turnover - Market Data", "Bet Time (UTC)"),
        # Top 4
        ("Fourth Customer by Turnover", "First Bet (UTC)"),
        ("Fourth Customer by Turnover - Market Data", "Bet Time (UTC)"),
        # Top 5
        ("Fifth Customer by Turnover", "First Bet (UTC)"),
        ("Fifth Customer by Turnover - Market Data", "Bet Time (UTC)"),
    ]

    df_dict = get_sheet_data(
        workbook=workbook,
        sheet_name=sheet_name,
        target_tables=targeted_tables,
        include_full_table_name=True,
    )

    formatted_dict = dict()
    keys = list(df_dict.keys())

    for i in range(0, len(keys), 2):
        key = keys[i]
        next_key = keys[i + 1]

        cleaned_key, customer_info = get_customer_key_splitted(key)
        cleaned_next_key, _ = get_customer_key_splitted(next_key)

        formatted_dict[customer_info] = {
            cleaned_key: df_dict[key],
            cleaned_next_key: df_dict[next_key],
        }

        total_customer_turnover = df_dict[next_key]["T/O"].sum()

        formatted_dict[customer_info][f"{cleaned_next_key} By Market"] = (
            df_dict[next_key]
            .groupby("Market")
            .agg(
                total_to=("T/O", "sum"),
                total_pl=("P/L", "sum"),
                won_count=("Result", lambda x: x.str.contains("Won", case=False).sum()),
                turnover_pct=("T/O", lambda x: x.sum() / total_customer_turnover),
                total_bets=("Result", "count"),
            )
            .rename(
                columns={
                    "total_to": "T/O",
                    "total_pl": "P/L",
                    "won_count": "Wins",
                    "total_bets": "Bets",
                    "turnover_pct": "Customer %",
                }
            )
            .reset_index()
        )

        formatted_dict[customer_info][f"{cleaned_next_key} By Selection"] = (
            df_dict[next_key]
            .groupby(["Market", "Selection"])
            .agg(
                total_to=("T/O", "sum"),
                total_pl=("P/L", "sum"),
                won_count=("Result", lambda x: x.str.contains("Won", case=False).sum()),
                turnover_pct=("T/O", lambda x: x.sum() / total_customer_turnover),
                total_bets=("Result", "count"),
            )
            .rename(
                columns={
                    "total_to": "T/O",
                    "total_pl": "P/L",
                    "won_count": "Wins",
                    "total_bets": "Bets",
                    "turnover_pct": "Customer %",
                }
            )
            .reset_index()
        )

    return formatted_dict
