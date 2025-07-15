import pandas as pd
import typing as t


def get_market_percentage(
    market: pd.Series,
    market_summary_data: t.Dict[str, pd.DataFrame],
    turnover_column: str = "Total T/O",
) -> float:
    # Filter by period
    period_market = ""
    if "1st quarter" in market["Market"]:
        df_filtered = market_summary_data["Market Summary - Singles - 1Q"]
        period_market = "1st quarter"
    elif "2nd quarter" in market["Market"]:
        df_filtered = market_summary_data["Market Summary - Singles - 2Q"]
        period_market = "2nd quarter"
    elif "3rd quarter" in market["Market"]:
        df_filtered = market_summary_data["Market Summary - Singles - 3Q"]
        period_market = "3rd quarter"
    elif "4th quarter" in market["Market"]:
        df_filtered = market_summary_data["Market Summary - Singles - 4Q"]
        period_market = "4th quarter"
    elif "1st half" in market["Market"]:
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
        totals_key = f"{period_market} - total" if period_market else "total"
        df_filtered = df_filtered[
            df_filtered["Market"].str.contains(totals_key, case=False, na=False)
        ]
    else:
        df_filtered = df_filtered[df_filtered["Market"] == market["Market"]]

    if not len(df_filtered) or not df_filtered["Total T/O"].sum():
        return 0

    return market[turnover_column] / df_filtered["Total T/O"].sum()


def get_selection_percentage(
    selection: pd.Series,
    market_analysis_data: pd.DataFrame,
    turnover_column: str = "Total T/O",
) -> float:
    # Filter by market and selection
    df_filtered = market_analysis_data[
        (market_analysis_data["Market"] == selection["Market"])
        & (market_analysis_data["Selection"] == selection["Selection"])
    ]

    if not len(df_filtered) or not df_filtered["Total T/O"].sum():
        return 0

    return selection[turnover_column] / df_filtered["Total T/O"].sum()
