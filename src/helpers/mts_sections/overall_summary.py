from openpyxl import Workbook
import typing as t
import pandas as pd

from helpers.excel import get_sheet_data


def get_overall_summary_data(workbook: Workbook) -> t.Dict[str, pd.DataFrame]:
    sheet_name = "Overall Summary"
    targeted_tables = [
        ("Accepted/Rejected Summary", "State"),
        ("PreMatch/Live Summary - Singles Only", "Pre/Live"),
    ]

    return get_sheet_data(
        workbook=workbook, sheet_name=sheet_name, target_tables=targeted_tables
    )
