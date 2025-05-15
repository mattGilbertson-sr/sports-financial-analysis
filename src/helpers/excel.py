from openpyxl import Workbook
import typing as t
import pandas as pd


def clean_number_values(val: t.Any) -> t.Any:
    if isinstance(val, str):
        val = val.replace("€", "").replace("%", "").replace(",", "").strip()
    return val


def find_table_data(
    sheet: t.List[t.List[t.Any]], table_name: str, first_column: str
) -> t.Tuple[t.Optional[pd.DataFrame], str]:
    table_found = False
    full_table_name = "undefined"
    columns = []
    data = []
    bets_cols_indexes = []

    for i, row in enumerate(sheet):
        if (
            isinstance(row[0], str) and table_name in row[0]
        ):  # Check if we found our table
            table_found = True
            full_table_name = row[0]
            continue
        elif not table_found:  # If the table name hasn't been found, we keep looking
            continue

        if not columns and first_column == row[0]:  # Check row with the columns
            columns = [col for col in row if col is not None]

            if "Bets" in columns and "Accepted Bets" in sheet[i - 1]:
                bets_cols_indexes = [i for i, x in enumerate(row) if x == "Bets"]
                columns = (
                    columns[: bets_cols_indexes[0]]
                    + [
                        f"Accepted {col}"
                        for col in columns[bets_cols_indexes[0] : bets_cols_indexes[1]]
                    ]
                    + [f"Rejected {col}" for col in columns[bets_cols_indexes[1] :]]
                )

            continue
        elif columns and row[0]:  # Start saving table data
            data.append([val for val in row if val is not None])
        elif columns:  # Table data ended
            break

    if not data:
        return None, full_table_name

    df = pd.DataFrame(data, columns=columns)

    # Apply to all object columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(clean_number_values)

        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    if bets_cols_indexes:
        generic_columns = [
            col.replace("Accepted ", "")
            for col in columns
            if "Accepted " in col and "Margin" not in col
        ]

        for col in generic_columns:
            if col == "Avg Stake":
                accepted_pct = df["Accepted Bets"] / df["Total Bets"]
                rejected_pct = df["Rejected Bets"] / df["Total Bets"]
                df["Total Avg Stake"] = (
                    df["Accepted Avg Stake"] * accepted_pct
                    + df["Rejected Avg Stake"] * rejected_pct
                )
            else:
                df[f"Total {col}"] = df[f"Accepted {col}"] + df[f"Rejected {col}"]

        df[f"Accepted Margin"] = df["Accepted P/L"] / df["Accepted T/O"]
        df[f"Rejected Margin"] = df["Rejected P/L"] / df["Rejected T/O"]
        df[f"Total Margin"] = df["Total P/L"] / df["Total T/O"]
    elif "Margin" in columns:
        df["Margin"] = df["P/L"] / df["T/O"]

    return df, full_table_name


def get_sheet_data(
    workbook: Workbook,
    sheet_name: str,
    target_tables: t.List[
        t.Tuple[str, str]
    ],  # Tuples are made of (table_name, first_column)
    include_full_table_name=False,
) -> t.Dict[str, pd.DataFrame]:
    sheet = workbook[sheet_name]
    data = [[cell.value for cell in row] for row in sheet.iter_rows()]

    sheet_data = dict()

    for table in target_tables:
        table_data, full_table_name = find_table_data(
            sheet=data, table_name=table[0], first_column=table[1]
        )
        if isinstance(table_data, pd.DataFrame):
            table_key = table[0] if table[0] != "undefined" else sheet_name
            sheet_data[full_table_name if include_full_table_name else table_key] = (
                table_data
            )

    return sheet_data
