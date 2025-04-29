from openpyxl import Workbook
import typing as t
import pandas as pd


# Function to clean monetary values
def clean_number_values(val):
    if isinstance(val, str):
        val = val.replace("€", "").replace("%", "").replace(",", "").strip()
    return val


def find_table_data(sheet, table_name, first_column):
    table_found = False
    columns = []
    data = []

    for i, row in enumerate(sheet):
        if (
            isinstance(row[0], str) and table_name in row[0]
        ):  # Check if we found our table
            table_found = True
            continue
        elif not table_found:  # If the table name hasn't been found, we keep looking
            continue

        if not columns and first_column == row[0]:  # Check row with the columns
            columns = [col for col in row if col is not None]

            if "Bets" in columns and "Accepted Bets" in sheet[i - 1]:
                indexes = [i for i, x in enumerate(row) if x == "Bets"]
                columns = (
                    columns[: indexes[0]]
                    + [f"Accepted {col}" for col in columns[indexes[0] : indexes[1]]]
                    + [f"Rejected {col}" for col in columns[indexes[1] :]]
                )

            continue
        elif columns and row[0]:  # Start saving table data
            data.append([val for val in row if val is not None])
        elif columns:  # Table data ended
            break

    if not data:
        return None

    df = pd.DataFrame(data, columns=columns)

    # Apply to all object columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(clean_number_values)
        
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    return df


def get_sheet_data(
    workbook: Workbook,
    sheet_name: str,
    target_tables: t.List[
        t.Tuple[str, str]
    ],  # Tuples are made of (table_name, first_column)
):
    sheet = workbook[sheet_name]
    data = [[cell.value for cell in row] for row in sheet.iter_rows()]

    sheet_data = dict()

    for table in target_tables:
        table_data = find_table_data(
            sheet=data, table_name=table[0], first_column=table[1]
        )
        if isinstance(table_data, pd.DataFrame):
            table_key = table[0] if table[0] != "undefined" else sheet_name
            sheet_data[table_key] = table_data

    return sheet_data
