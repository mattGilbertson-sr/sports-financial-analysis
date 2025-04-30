import streamlit as st
import pandas as pd
from streamlit import column_config


def set_session_state(wb, session_state_key, data_function, uploaded_file_name):
    if (
        session_state_key not in st.session_state
        or uploaded_file_name != st.session_state.get("file_name")
    ):
        st.session_state[session_state_key] = data_function(wb)

    return st.session_state[session_state_key]


def style_df(df: pd.DataFrame):
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


def display_data_dict(title: str, tab, data_dict: dict[str, pd.DataFrame]):
    with tab:
        for key, df in data_dict.items():
            with st.expander(f"{key}", expanded=False):
                # Automatically generate column configs for numeric columns
                col_config = {}
                for col in df.select_dtypes(include="number").columns:
                    col_format = "%d"

                    if not pd.api.types.is_integer_dtype(df[col]) and "Margin" in col:
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
