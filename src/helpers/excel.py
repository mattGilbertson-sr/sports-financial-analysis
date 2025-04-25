from openpyxl import Workbook
import typing as t
import pandas as pd


def find_table_data(sheet, table_name, first_column):
    table_found = False
    columns = []
    data = []

    for row in sheet:
        if table_name in row:  # Check if we found our table
            table_found = True
            continue
        elif not table_found:  # If the table name hasn't been found, we keep looking
            continue

        if not columns and first_column == row[0]:  # Check row with the columns
            columns = [col for col in row if col is not None]
            continue
        elif columns and row[0]:  # Start saving table data
            data.append([val for val in row if val is not None])
        elif columns:  # Table data ended
            break

    return pd.DataFrame(data, columns=columns)


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
        sheet_data[table[0]] = find_table_data(
            sheet=data, table_name=table[0], first_column=table[1]
        )

    return sheet_data
