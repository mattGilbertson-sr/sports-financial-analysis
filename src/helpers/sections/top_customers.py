from openpyxl import Workbook
import typing as t
import pandas as pd

from helpers.excel import get_sheet_data
from helpers.market_percentage import get_market_percentage, get_selection_percentage


def get_customer_key_splitted(key: str) -> t.Tuple[str, str]:
    if "Bookmaker" not in key:
        return key

    bookmaker_index = key.index("Bookmaker")

    return key[:bookmaker_index], key[bookmaker_index:]


def get_top_customers_data(
    workbook: Workbook,
    market_summary_data: t.Dict[str, pd.DataFrame],
    market_analysis_data: t.Dict[str, pd.DataFrame],
) -> t.Dict[str, pd.DataFrame]:
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

    # Format the customer display
    for i in range(0, len(keys), 2):
        key = keys[i]
        next_key = keys[i + 1]

        # Convert the total margin to the right format of the streamlit percentage display
        try:
            # Handle common percentage formats like "15%", "0.15", etc.
            margin_col = df_dict[key]["Total Margin"]

            # If it's already a string with %, remove the % and convert
            if margin_col.dtype == "object":  # String column
                # Remove % symbol if present and convert to numeric
                margin_col = margin_col.astype(str).str.replace("%", "").str.strip()
                df_dict[key]["Total Margin"] = (
                    pd.to_numeric(margin_col, errors="coerce") / 100
                )
            else:
                # If already numeric, just divide
                df_dict[key]["Total Margin"] = df_dict[key]["Total Margin"] / 100

        except Exception as e:
            print(f"Error processing Total Margin for {key}: {e}")
            # Set to 0 or handle as needed
            df_dict[key]["Total Margin"] = 0

        cleaned_key, customer_info = get_customer_key_splitted(key)
        cleaned_next_key, _ = get_customer_key_splitted(next_key)

        formatted_dict[customer_info] = {
            cleaned_key: df_dict[key],  # Customer history information
            cleaned_next_key: df_dict[next_key],  # Customer turnover data for the match
        }

        total_customer_turnover = df_dict[next_key]["T/O"].sum()

        # Customer bets aggreagated by market
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

        # How much of that market did this customer account for
        formatted_dict[customer_info][f"{cleaned_next_key} By Market"][
            "Market %"
        ] = formatted_dict[customer_info][f"{cleaned_next_key} By Market"].apply(
            lambda x: get_market_percentage(
                x, market_summary_data, turnover_column="T/O"
            ),
            axis=1,
        )

        # Customer bets aggregated by selection
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

        # How much of that selection did this customer account for
        formatted_dict[customer_info][f"{cleaned_next_key} By Selection"][
            "Selection %"
        ] = formatted_dict[customer_info][f"{cleaned_next_key} By Selection"].apply(
            lambda x: get_selection_percentage(
                x,
                market_analysis_data["Market Analysis - Singles"],
                turnover_column="T/O",
            ),
            axis=1,
        )

        # How much of that market did this customer account for with this selection
        formatted_dict[customer_info][f"{cleaned_next_key} By Selection"][
            "Market %"
        ] = formatted_dict[customer_info][f"{cleaned_next_key} By Selection"].apply(
            lambda x: get_market_percentage(
                x, market_summary_data, turnover_column="T/O"
            ),
            axis=1,
        )

    return formatted_dict
