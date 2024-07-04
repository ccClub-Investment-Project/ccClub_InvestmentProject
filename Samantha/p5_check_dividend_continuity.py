
# part 5: dividend continuity check:
'''dividend check: consistently paid cash dividends in each of the 3 fiscal years'''


# step 1. Transform data into positive numbers
# step 2. delete stocks in financial_dividend_data.csv that do not exist in filtered_by_net_income.csv


import pandas as pd

# 讀取並處理 financial_dividend_data.csv 檔案
df = pd.read_csv('web_scraping_raw_data/financial_dividend_data.csv', dtype=str)

# 處理季度欄位
quarters = ['109季', '110季', '111季', '112季']
for q in quarters:
    df[q] = df[q].apply(lambda x: abs(int(float(x.replace(',', '').replace('"', '').replace('-', '')))) if isinstance(x, str) else x)

# 刪除任何一個季度數字為零的整行
df = df[~df[quarters].eq('0').any(axis=1)]

# 儲存處理過的檔案
df.to_csv('web_scraping_raw_data/processed_financial_dividend_data.csv', index=False)

# 讀取處理過的 financial_dividend_data.csv 檔案
df_processed_dividend = pd.read_csv('web_scraping_raw_data/processed_financial_dividend_data.csv')

# 讀取 filtered_by_net_income.csv 檔案
df_net_income = pd.read_csv('web_scraping_raw_data/filtered_by_net_income.csv')

# 確保兩個 DataFrame 有相同的索引以便對齊
df_processed_dividend = df_processed_dividend.reset_index(drop=True)
df_net_income = df_net_income.reset_index(drop=True)

# 從 net income 資料中取得股票代號集合
net_income_tickers = set(df_net_income['代號'])

# 根據 net income 資料中的股票代號來篩選處理過的股利資料
df_filtered_dividend = df_processed_dividend[df_processed_dividend['代號'].isin(net_income_tickers)]

# 儲存篩選後的資料
df_filtered_dividend.to_csv('web_scraping_raw_data/filtered_financial_dividend_data.csv', index=False)

