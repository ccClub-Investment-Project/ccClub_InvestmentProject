from app_tools.pickle_handler import save_data, load_data
import yfinance as yf
import pandas as pd

def fetch_stock_data(stock_id):
    df = yf.download(stock_id)
    df.reset_index(inplace=True)
    return df

def get_history(codes):
    # all_yield = load_data("all_yield")
    tpex_listed = load_data("tpex_listed")
    twse_listed = load_data("twse_listed")
    # 將代號轉換為數字
    tpex_listed['code'] = tpex_listed['code'].apply(pd.to_numeric, errors='coerce')
    twse_listed['code'] = twse_listed['code'].apply(pd.to_numeric, errors='coerce')

    all_history = {}
    for code in codes:
        stock_id = ""
        if code in twse_listed['code'].values:
            # print(f"{code} use TW")
            stock_id = f"{code}.TW"
        elif code in tpex_listed['code'].values:
            # print(f"{code} use TWO")
            stock_id = f"{code}.TWO"
        else:
            print(f"could not find {code}")
        df = fetch_stock_data(stock_id)
        all_history[stock_id] = df
        # all_yield = load_data("all_yield")
    return all_history

def get_etf_history():
    etf_domestic_list = load_data("etf_domestic_list")
    all_history = {}
    for etf in etf_domestic_list:
        code = etf['code']
        stock_id = f"{code}.TW"
        df = fetch_stock_data(stock_id)
        all_history[stock_id] = df
    return all_history