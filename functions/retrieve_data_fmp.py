from urllib.request import urlopen
from datetime import datetime
import pandas as pd
import json
import math


def fmp_json_retrieve_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


def fmp_get_all_tickers(api_key):
    url = "https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=" + api_key
    return fmp_json_retrieve_data(url)


def fmp_get_income_statement(ticker, api_key):
    url = "https://financialmodelingprep.com/api/v3/income-statement/" + ticker + "?apikey=" + api_key
    return fmp_json_retrieve_data(url)


def fmp_get_all_quotes(api_key, tickers_per_batch=750):
    # Get all available tickers
    all_tickers = fmp_get_all_tickers(api_key)  # Entire quote list
    all_tickers = [s.replace("^", "") for s in all_tickers]  # Remove unwanted characters
    all_tickers = [s.replace("/", "") for s in all_tickers]  # Remove unwanted characters
    all_tickers.remove("ALICORC1.LM")  # This ticker does not exist in FMP

    # Iterate through several batch requests to obtain full list of stock quotes
    print("-------------------------------------------------")
    print("Fetching quotes from Financial Modelling Prep")
    print("Number of tickers: " + str(len(all_tickers)))
    print("Tickers per batch: " + str(tickers_per_batch))
    print("API key: " + api_key)
    print("-------------------------------------------------")

    quote_batch = list()
    batch_count = 0
    for ind in range(0, math.ceil(len(all_tickers) / tickers_per_batch)):
        batch_count = batch_count + 1
        nr_quotes_before = len(quote_batch)
        quote_batch = quote_batch + fmp_json_retrieve_data("https://financialmodelingprep.com/api/v3/quote/" +
                                                           ','.join(all_tickers
                                                            [tickers_per_batch * ind:tickers_per_batch * (ind + 1)]) +
                                                           "?apikey=" + api_key)
        print("Loaded from FMP quote " + str(nr_quotes_before) + " to " + str(len(quote_batch)))

    print("\n" + str(len(quote_batch)) + " quotes successfully loaded from FMP in "  + str(batch_count) + " batches")

    # Convert to pandas DataFrame
    fmp_quotes = pd.DataFrame(quote_batch)  # Create dataframe
    fmp_quotes.index = fmp_quotes["symbol"]  # Use ticker symbol as DataFrame index
    return fmp_quotes


def fmp_save_quotes_to_csv(fmp_quotes, filename="fmp_quotes"):
    now = datetime.now()
    filename_full = "data/" + filename + "_" + now.strftime("%y%m%d%H%M") + ".csv"
    fmp_quotes.to_csv(filename_full, index_label="index")
    print("FMP quotes saved to " + filename_full)
