

# 先用歷史資料
#
#
# import pandas as pd
#
# # 讀取 filtered_financial_dividend_data.csv 檔案，取得 112 季的資料
# df_dividend_data = pd.read_csv('web_scraping_raw_data/filtered_financial_dividend_data.csv', dtype=str)
# df_dividend_data = df_dividend_data[['代號', '112季']]  # 只取 112 季的資料
#
# # 讀取 stock_data_for_div_yield_calculation.csv 檔案
# df_stock_data = pd.read_csv('web_scraping_raw_data/stock_data_for_div_yield_calculation.csv', dtype=str)
#
# # 將發行量從字串轉換為整數
# df_stock_data['發行量(股)'] = df_stock_data['發行量(股)'].astype(int)
#
# # 將股票資料與股利資料合併
# df_merged = pd.merge(df_stock_data, df_dividend_data, on='代號', how='inner')
#
# # 計算每股股利（112季 / 發行量(股)）
# df_merged['dividend_per_share'] = df_merged['112季'].astype(float) / df_merged['發行量(股)']
#
# # 將計算後的結果存儲為新的 CSV 檔案
# df_merged.to_csv('web_scraping_raw_data/stock_data_with_dividend_per_share.csv', index=False)
