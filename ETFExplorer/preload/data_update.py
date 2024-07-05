from collection.api_data import get_news_data, api_table_data, get_strategy_yield, get_all_plot_data

from app_tools.pickle_handler import save_data, load_data
from collection.crawler.stock_list import get_twse, get_tpex
from collection.crawler.stock_history import get_history

import pandas as pd


def update_from_api():
    # 從api 更新數據 並存至pickle
    etf_domestic_list = api_table_data('etf_domestic_list')
    save_data(etf_domestic_list,'etf_domestic_list')
    # 從api 更新數據 並存至pickle
    etf_performance = api_table_data('etf_performance')
    save_data(etf_performance,'etf_performance')
    # 從api 更新數據 並存至pickle
    all_yield = get_strategy_yield(0)
    save_data(all_yield,'all_yield')
    print("從api下載完畢並存至pickle")

def update_from_crawler():
    twse_listed = get_twse()
    save_data(twse_listed,'twse_listed')
    tpex_listed = get_tpex()
    save_data(tpex_listed,'tpex_listed')

    # 下載前四個條件篩選的資料
    all_yield = load_data("all_yield")
    codes = [pd.to_numeric(stock['代號'], errors='coerce') for stock in all_yield]
    all_history = get_history(codes)
    save_data(all_history,'all_history')

    print("從crawler下載完畢並存至pickle")
