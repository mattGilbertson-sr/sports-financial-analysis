import streamlit as st
import typing as t
import pandas as pd
from openpyxl import Workbook
from streamlit import column_config


def set_session_state(
    wb: Workbook,
    session_state_key: str,
    data_function: t.Callable,
    uploaded_file_name: str,
    **kwargs,
) -> t.Any:
    if (
        session_state_key not in st.session_state
        or uploaded_file_name != st.session_state.get("file_name")
    ):
        st.session_state[session_state_key] = data_function(wb, **kwargs)

    return st.session_state[session_state_key]


def style_df(df: pd.DataFrame) -> pd.DataFrame:
    columns = df.columns

    green_cols = [col for col in columns if "Accepted " in col]
    red_cols = [col for col in columns if "Rejected " in col]
    blue_cols = [col for col in columns if "Total " in col]

    return (
        df.style.apply(
            lambda x: ["background-color: lightgreen; color: black" for _ in x],
            subset=green_cols,
        )
        .apply(
            lambda x: ["background-color: red; color: black" for _ in x],
            subset=red_cols,
        )
        .apply(
            lambda x: ["background-color: lightblue; color: black" for _ in x],
            subset=blue_cols,
        )
    )


def display_streamlit_df(df: pd.DataFrame) -> None:
    # Automatically generate column configs for numeric columns
    col_config = {}
    for col in df.select_dtypes(include="number").columns:
        col_format = "%d"

        if not pd.api.types.is_integer_dtype(df[col]) and (
            "Margin" in col or "%" in col
        ):
            col_format = "percent"
        elif not pd.api.types.is_integer_dtype(df[col]):
            col_format = "euro"

        col_config[col] = column_config.NumberColumn(format=col_format)

    # Display with formatting (but keep columns as numeric types)
    st.dataframe(
        style_df(df),
        column_config=col_config,
        use_container_width=True,
        hide_index=True,
    )


def display_data_dict(tab, data_dict: dict[str, pd.DataFrame]) -> None:
    with tab:
        for key, val in data_dict.items():
            if isinstance(val, pd.DataFrame):
                with st.expander(f"{key}", expanded=False):
                    display_streamlit_df(val)
            elif isinstance(val, dict):
                st.subheader(key)

                for sub_key, sub_df in val.items():
                    with st.expander(f"{sub_key}", expanded=False):
                        display_streamlit_df(sub_df)
