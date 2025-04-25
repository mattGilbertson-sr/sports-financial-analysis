from openpyxl import load_workbook
from pathlib import Path
from helpers.overall_summary import get_overall_summary_data
from helpers.market_cluster import get_market_cluster_data

# Define the file path
file_name = "20250423_SCBrasilCapixabaES_PortoVitoriaFCES_60021497"
file_path = Path(__file__).parents[1] / "dist" / f"{file_name}.xlsx"

# Load the workbook
wb = load_workbook(file_path, data_only=True)

data = get_market_cluster_data(wb)
print(data)
