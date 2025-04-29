from openpyxl import load_workbook
from pathlib import Path
from helpers import mts_sections as mts
import pandas as pd
import streamlit as st

# Define the file path
file_name = "20250423_SCBrasilCapixabaES_PortoVitoriaFCES_60021497"
file_path = Path(__file__).parents[1] / "dist" / f"{file_name}.xlsx"

st.set_page_config(layout="wide")

st.title("Cartola FC Analytics")

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


def display_data_dict(title: str, data_dict: dict[str, pd.DataFrame]):
    st.subheader(title)
    for key, df in data_dict.items():
        with st.expander(f"{key}", expanded=False):
            st.dataframe(df)


display_data_dict("Overall Summary", overall_summary_data)
display_data_dict("Market Cluster", market_cluster_data)
display_data_dict("Market Summary", market_summary_data)
display_data_dict("Market Analysis", market_analysis_data)
display_data_dict("Customer Summary", customer_summary_data)
display_data_dict("Top Customers", top_customers_data)
display_data_dict("Period Summary", period_summary_data)
display_data_dict("Score Summary", score_summary_data)
display_data_dict("CCF Category Summary", ccf_category_data)
