from functions.retrieve_data_fmp import *


# ---------------------- Configuration ----------------------
config = dict()
config["retrieve_fmp_data"] = True  # Generate data from FMP
config["save_fmp_data"] = True  # Save FMP quote data to CSV file
config["fmp_quotes_file"] = "fmp_quotes_2111282042.csv"  # CSV file to load FMP quote data

# ---------------------- From FMP ----------------------
# FMP API keys
api_key_fmp = "1d5f2b76686c208084ad943923c6c8c3"  # ismaelmatamoros@gmail.com
# api_key_fmp = "dea2bd3cdbfe04bb4d482760055043c9"  # ismaelmatamoros@hotmail.com

# Generate or load raw data
if config["retrieve_fmp_data"]:
    fmp_quotes_raw = fmp_get_all_quotes(api_key_fmp)
    if config["save_fmp_data"]: fmp_save_quotes_to_csv(fmp_quotes_raw, filename="fmp_quotes_raw")
else:
    fmp_quotes_raw = pd.read_csv("data/" + config["fmp_quotes_file"], index_col=0)
