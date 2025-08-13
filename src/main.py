from openpyxl import load_workbook
from helpers import sections
import pandas as pd
import streamlit as st

from helpers.streamlit import display_data_dict, set_session_state

tabs = {
    "Overall Summary": None,
    "Bookmaker Summary": None,
    "Top Bookmakers": None,
    "Market Cluster": None,
    "Market Summary": None,
    "Market Analysis": None,
    "Customer Summary": None,
    "Top Customers": None,
    "Period Summary": None,
    "Score Summary": None,
    "CCF Category Summary": None,
}

pd.options.mode.chained_assignment = None  # default='warn'

st.set_page_config(layout="wide")
st.title("Sports Financial Analysis")

# Upload the file
uploaded_file = st.file_uploader("Upload the .xlsx file", type=["xlsx"])

if uploaded_file:
    uploaded_file_name = uploaded_file.name

    # Load the workbook from the uploaded file
    wb = load_workbook(uploaded_file, data_only=True)

    # Overall Summary
    tabs["Overall Summary"] = set_session_state(
        wb,
        "overall_summary_data",
        sections.get_overall_summary_data,
        uploaded_file_name,
    )

    if not tabs["Overall Summary"]:
        st.error("❌ The uploaded file is not valid.")
        st.stop()

    # Get total match turnover from the Overall Summary
    total_match_turnover = tabs["Overall Summary"][
        "PreMatch/Live Summary - Singles Only"
    ]["Total T/O"].sum()

    # Get the rest of the tabs data
    tabs["Market Cluster"] = set_session_state(
        wb,
        "market_cluster_data",
        sections.get_market_cluster_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    tabs["Bookmaker Summary"] = set_session_state(
        wb,
        "bookmaker_summary_data",
        sections.get_bookmaker_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    tabs["Market Summary"] = set_session_state(
        wb,
        "market_summary_data",
        sections.get_market_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    tabs["Top Bookmakers"] = set_session_state(
        wb,
        "top_bookmakers_data",
        sections.get_top_bookmakers_data,
        uploaded_file_name,
        market_summary_data=tabs["Market Summary"],
        total_match_turnover=total_match_turnover,
    )
    tabs["Market Analysis"] = set_session_state(
        wb,
        "market_analysis_data",
        sections.get_market_analysis_data,
        uploaded_file_name,
        market_summary_data=tabs["Market Summary"],
        total_match_turnover=total_match_turnover,
    )
    tabs["Customer Summary"] = set_session_state(
        wb,
        "customer_summary_data",
        sections.get_customer_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    tabs["Top Customers"] = set_session_state(
        wb,
        "top_customers_data",
        sections.get_top_customers_data,
        uploaded_file_name,
        market_summary_data=tabs["Market Summary"],
        market_analysis_data=tabs["Market Analysis"],
    )
    tabs["Period Summary"] = set_session_state(
        wb,
        "period_summary_data",
        sections.get_period_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    tabs["Score Summary"] = set_session_state(
        wb,
        "score_summary_data",
        sections.get_score_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )
    tabs["CCF Category Summary"] = set_session_state(
        wb,
        "ccf_category_data",
        sections.get_ccf_category_summary_data,
        uploaded_file_name,
        total_match_turnover=total_match_turnover,
    )

    # Only generate tabs if there is valid data for display
    streamlit_tabs = st.tabs(
        [tab_key for tab_key, tab_data in tabs.items() if tab_data is not None]
    )

    with streamlit_tabs[0]:
        st.metric(label="Total Match Turnover", value=f"€{total_match_turnover:,.2f}")

    tabs_index_counter = 0

    for tab_data in tabs.values():
        if not tab_data:
            continue

        display_data_dict(streamlit_tabs[tabs_index_counter], tab_data)
        tabs_index_counter += 1

    st.session_state.file_name = uploaded_file.name
