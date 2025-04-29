from openpyxl import load_workbook
from pathlib import Path
from helpers import mts_sections as mts
import pandas as pd
import streamlit as st
from streamlit import column_config

# Define the file path
file_name = "20250423_SCBrasilCapixabaES_PortoVitoriaFCES_60021497"
file_path = Path(__file__).parents[1] / "dist" / f"{file_name}.xlsx"

st.set_page_config(layout="wide")

st.title("MTS Analysis")

# Load the workbook
wb = load_workbook(file_path, data_only=True)


def set_session_state(wb, session_state_key, data_function):
    if session_state_key not in st.session_state:
        st.session_state[session_state_key] = data_function(wb)

    return st.session_state[session_state_key]


overall_summary_data = set_session_state(
    wb, "overall_summary_data", mts.get_overall_summary_data
)
market_cluster_data = set_session_state(
    wb, "market_cluster_data", mts.get_market_cluster_data
)
market_summary_data = set_session_state(
    wb, "market_summary_data", mts.get_market_summary_data
)
market_analysis_data = set_session_state(
    wb, "market_analysis_data", mts.get_market_analysis_data
)
customer_summary_data = set_session_state(
    wb, "customer_summary_data", mts.get_customer_summary_data
)
top_customers_data = set_session_state(
    wb, "top_customers_data", mts.get_top_customers_data
)
period_summary_data = set_session_state(
    wb, "period_summary_data", mts.get_period_summary_data
)
score_summary_data = set_session_state(
    wb, "score_summary_data", mts.get_score_summary_data
)
ccf_category_data = set_session_state(
    wb, "ccf_category_data", mts.get_ccf_category_summary_data
)


def display_data_dict(title: str, tab, data_dict: dict[str, pd.DataFrame]):
    # st.subheader(title)
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
                    df,
                    column_config=col_config,
                    use_container_width=True,
                    hide_index=True,
                )


tabs = [
    "Overall Summary",
    "Market Cluster",
    "Market Summary",
    "Market Analysis",
    "Customer Summary",
    "Top Customers",
    "Period Summary",
    "Score Summary",
    "CCF Category Summary",
]

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(tabs)

display_data_dict(tabs[0], tab1, overall_summary_data)
display_data_dict(tabs[1], tab2, market_cluster_data)
display_data_dict(tabs[2], tab3, market_summary_data)
display_data_dict(tabs[3], tab4, market_analysis_data)
display_data_dict(tabs[4], tab5, customer_summary_data)
display_data_dict(tabs[5], tab6, top_customers_data)
display_data_dict(tabs[6], tab7, period_summary_data)
display_data_dict(tabs[7], tab8, score_summary_data)
display_data_dict(tabs[8], tab9, ccf_category_data)
