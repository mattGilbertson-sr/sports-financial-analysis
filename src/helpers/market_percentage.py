import pandas as pd
import typing as t

periods_dict = {
    # Halves
    "1st half": "1H",
    "2nd half": "2H",
    # Quarters
    "1st quarter": "1Q",
    "2nd quarter": "2Q",
    "3rd quarter": "3Q",
    "4th quarter": "4Q",
    # Sets
    "1st set": "1S",
    "2nd set": "2S",
    "3rd set": "3S",
    "4th set": "4S",
    "5th set": "5S",
}


def get_market_dicts_by_period(market_key: str, df: pd.DataFrame) -> dict:
    df_dict = dict()

    # Dynamically exclude all period-specific rows to get "Full Time"
    mask = ~df["Market"].str.contains(
        "|".join(periods_dict.keys()), case=False, na=False
    )
    df_dict[f"{market_key} - FT"] = df[mask]

    # Get the markets by period
    for period_key, period_abbreviation in periods_dict.items():
        df_dict[f"{market_key} - {period_abbreviation}"] = df[
            df["Market"].str.contains(period_key, case=False, na=False)
        ]

    return df_dict


def get_market_percentage(
    market: pd.Series,
    market_summary_data: t.Dict[str, pd.DataFrame],
    turnover_column: str = "Total T/O",
) -> float:
    # Filter by period
    period_market = ""
    for period_key, period_abbreviation in periods_dict.items():
        if period_key in market["Market"]:
            df_filtered = market_summary_data[
                f"Market Summary - Singles - {period_abbreviation}"
            ]
            period_market = period_key

    if not period_market:
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
