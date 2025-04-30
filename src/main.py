from openpyxl import load_workbook
from helpers import mts_sections as mts
import streamlit as st

from helpers.streamlit import display_data_dict, set_session_state

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
    market_cluster_data = set_session_state(
        wb, "market_cluster_data", mts.get_market_cluster_data, uploaded_file_name
    )
    market_summary_data = set_session_state(
        wb, "market_summary_data", mts.get_market_summary_data, uploaded_file_name
    )
    market_analysis_data = set_session_state(
        wb, "market_analysis_data", mts.get_market_analysis_data, uploaded_file_name
    )
    customer_summary_data = set_session_state(
        wb, "customer_summary_data", mts.get_customer_summary_data, uploaded_file_name
    )
    top_customers_data = set_session_state(
        wb, "top_customers_data", mts.get_top_customers_data, uploaded_file_name
    )
    period_summary_data = set_session_state(
        wb, "period_summary_data", mts.get_period_summary_data, uploaded_file_name
    )
    score_summary_data = set_session_state(
        wb, "score_summary_data", mts.get_score_summary_data, uploaded_file_name
    )
    ccf_category_data = set_session_state(
        wb, "ccf_category_data", mts.get_ccf_category_summary_data, uploaded_file_name
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

    st.session_state.file_name = uploaded_file.name
