from collection.api_data import get_news_data, api_table_data, get_strategy_yield, get_all_plot_data

from app_tools.pickle_handler import save_data, load_data
from collection.crawler.stock_list import get_twse, get_tpex
from collection.crawler.stock_history import get_history, get_etf_history

import pandas as pd
from datetime import datetime, timedelta


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
    twse_listed = twse_listed[['code']]
    save_data(twse_listed,'twse_listed')
    tpex_listed = get_tpex()
    tpex_listed = tpex_listed[['code']]
    save_data(tpex_listed,'tpex_listed')

    # 設置日期範圍為過去 10 年
    ten_years_ago = datetime.now() - timedelta(days=365 * 10)

    # 保留每個 DataFrame 中的 date 和 close 欄位，並限制日期在過去 10 年內
    def filter_df(df):
        if {'date', 'close'}.issubset(df.columns):
            df['date'] = pd.to_datetime(df['date'])
            return df[(df['Date'] >= ten_years_ago)][['Date', 'Close']]
        return df




    # 下載前四個條件篩選的資料
    all_yield = load_data("all_yield")
    codes = [pd.to_numeric(stock['代號'], errors='coerce') for stock in all_yield]
    all_history = get_history(codes)
    all_history_filter = {key: filter_df(df) for key, df in all_history.items()}

    save_data(all_history_filter,'all_history')
    all_etf_history = get_etf_history()
    all_etf_history_filter = {key: filter_df(df) for key, df in all_etf_history.items()}
    save_data(all_etf_history_filter,'all_etf_history')

    print("從crawler下載完畢並存至pickle")
