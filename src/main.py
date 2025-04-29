from openpyxl import load_workbook
from pathlib import Path
from helpers import mts_sections as mts

# Define the file path
file_name = "20250423_SCBrasilCapixabaES_PortoVitoriaFCES_60021497"
file_path = Path(__file__).parents[1] / "dist" / f"{file_name}.xlsx"

# Load the workbook
wb = load_workbook(file_path, data_only=True)

overall_summary_data = mts.get_overall_summary_data(wb)
market_cluster_data = mts.get_market_cluster_data(wb)
market_summary_data = mts.get_market_summary_data(wb)
market_analysis_data = mts.get_market_analysis_data(wb)
customer_summary_data = mts.get_customer_summary_data(wb)
top_customers_data = mts.get_top_customers_data(wb)
period_summary_data = mts.get_period_summary_data(wb)
score_summary_data = mts.get_score_summary_data(wb)
ccf_category_data = mts.get_ccf_category_summary_data(wb)

print("\nOverall Summary")
print(overall_summary_data)

print("\nMarket Cluster")
print(market_cluster_data)

print("\nMarket Summary")
print(market_summary_data)

print("\nMarket Analysis")
print(market_analysis_data)

print("\nCustomer Summary")
print(customer_summary_data)

print("\nTop Customers")
print(top_customers_data)

print("\nPeriod Summary")
print(period_summary_data)

print("\nScore Summary")
print(score_summary_data)

print("\nCCF Category Summary")
print(ccf_category_data)
