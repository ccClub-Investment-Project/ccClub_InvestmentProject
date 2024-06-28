import pandas as pd
from twstock import Stock

# 讀取 top_mar_cap_companies.csv 檔案
df_top = pd.read_csv('web_scraping_raw_data/top_mar_cap_companies.csv', dtype=str)

# 讀取 dividend_payout_ratios.csv 檔案，選擇要保留的公司代號
df_dividend = pd.read_csv('web_scraping_raw_data/dividend_payout_ratios.csv', dtype=str)
df_top_filtered = df_top[df_top['代號'].isin(df_dividend['代號'])]

# 將發行量從萬張換成股
df_top_filtered['發行量(股)'] = df_top_filtered['發行量(萬張)'].astype(float) * 10000
df_top_filtered['發行量(股)'] = df_top_filtered['發行量(股)'].astype(int)

# 刪除不需要的列
df_top_filtered.drop(columns=['市值(億)', '掛牌年數', '發行量(萬張)'], inplace=True)

# 使用 twstock 庫來獲取最新股價及日期
df_latest_prices = pd.DataFrame(columns=['代號', '股價', '日期'])

for idx, row in df_top_filtered.iterrows():
    stock_code = row['代號']
    stock = Stock(stock_code)
    if stock.price:
        latest_price = stock.price[-1]  # 取最新的股價
        price_date = stock.date[-1]  # 取最新股價的日期
        df_temp = pd.DataFrame({'代號': [stock_code], '股價': [latest_price], '日期': [price_date]})
        df_latest_prices = pd.concat([df_latest_prices, df_temp], ignore_index=True)

# 合併最新股價資料
df_merged = pd.merge(df_top_filtered, df_latest_prices, on='代號', how='inner')

# 存儲修改後的資料
df_merged.to_csv('web_scraping_raw_data/stock_data_for_div_yield_calculation.csv', index=False)
