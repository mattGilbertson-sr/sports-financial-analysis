from openpyxl import load_workbook
from helpers import mts_sections as mts
import pandas as pd
import streamlit as st

from helpers.streamlit import display_data_dict, set_session_state

pd.options.mode.chained_assignment = None  # default='warn'

st.set_page_config(layout="wide")
st.title("MTS Analysis")

# Upload the file
uploaded_file = st.file_uploader("Upload the .xlsx file", type=["xlsx"])

if uploaded_file:
    uploaded_file_name = uploaded_file.name

    # Load the workbook from the uploaded file
    wb = load_workbook(uploaded_file, data_only=True)

    overall_summary_data = set_session_state(
        wb, "overall_summary_data", mts.get_overall_summary_data, uploaded_file_name
    )

    total_match_turnover = overall_summary_data["PreMatch/Live Summary - Singles Only"][
        "Total T/O"
    ].sum()

    market_cluster_data = set_session_state(
        wb,
        "market_cluster_data",
        mts.get_market_cluster_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    market_summary_data = set_session_state(
        wb,
        "market_summary_data",
        mts.get_market_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    market_analysis_data = set_session_state(
        wb,
        "market_analysis_data",
        mts.get_market_analysis_data,
        uploaded_file_name,
        market_summary_data=market_summary_data,
        total_match_turnover=total_match_turnover,
    )
    customer_summary_data = set_session_state(
        wb,
        "customer_summary_data",
        mts.get_customer_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    top_customers_data = set_session_state(
        wb, "top_customers_data", mts.get_top_customers_data, uploaded_file_name
    )
    period_summary_data = set_session_state(
        wb,
        "period_summary_data",
        mts.get_period_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    score_summary_data = set_session_state(
        wb,
        "score_summary_data",
        mts.get_score_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    ccf_category_data = set_session_state(
        wb,
        "ccf_category_data",
        mts.get_ccf_category_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
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

    with tab1:
        st.metric(label="Total Match Turnover", value=f"€{total_match_turnover:,.2f}")

    display_data_dict(tab1, overall_summary_data)
    display_data_dict(tab2, market_cluster_data)
    display_data_dict(tab3, market_summary_data)
    display_data_dict(tab4, market_analysis_data)
    display_data_dict(tab5, customer_summary_data)
    display_data_dict(tab6, top_customers_data)
    display_data_dict(tab7, period_summary_data)
    display_data_dict(tab8, score_summary_data)
    display_data_dict(tab9, ccf_category_data)

    st.session_state.file_name = uploaded_file.name
