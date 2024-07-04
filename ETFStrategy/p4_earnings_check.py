


# Part 4:  earnings check:
'''the sum of operating income trailing four seasons is positive 近四季營業利益總和為正數'''

import pandas as pd

# 讀取 filtered_average_turnovers.csv 並提取 ticker 列
ticker_file = 'web_scraping_raw_data/filtered_average_turnovers.csv'
df_ticker = pd.read_csv(ticker_file)
tickers = df_ticker['ticker'].tolist()

# 讀取 financial_net_data_2.csv
financial_file = 'web_scraping_raw_data/financial_net_data2.csv'
df_financial = pd.read_csv(financial_file)

# # 去除逗號並將 '112季' 列轉換為浮點數
# df_financial['112季'] = df_financial['112季'].str.replace(",", "").astype(float)

# 處理季度欄位
quarters = ['109季', '110季', '111季', '112季']
for q in quarters:
    df_financial[q] = df_financial[q].apply(lambda x: abs(int(float(x.replace(',', '').replace('"', '').replace('-', '')))) if isinstance(x, str) else x)


# 篩選出代號在 ticker 列中的資料，且 '112季' > 0
filtered_df = df_financial[df_financial['代號'].isin(tickers) & (df_financial['112季'] > 0)]

# 將篩選出的資料另存成一個新的 CSV 檔案
output_file = 'web_scraping_raw_data/filtered_by_net_income.csv'
filtered_df.to_csv(output_file, index=False)

print("篩選後的資料已存成:", output_file)


# # 讀取包含股票代號的CSV文件，並指定名稱和代號欄位
# ticker_file = 'web_scraping_raw_data/filtered_average_turnovers.csv.csv'
# df_ticker = pd.read_csv(ticker_file, usecols=['ticker'])
#
#
# # 讀取 CSV 文件
# df = pd.read_csv(input_csv_file)
#
# # 過濾掉 average_turnover 小於 100,000,000 的股票
# filtered_df = df[df['average_turnover'] >= 100000000]
#
# # 將過濾後的數據輸出為 CSV 文件
# filtered_df.to_csv(output_csv_file, index=False)
#
# print("完成過濾並輸出到新的 CSV 文件。")
#
#

def calculate_div_yield(ticker):
    '''The forcast dividend yield can be calculated as
       1) dividend from FY23/stock price, or
       2) 最近4季EPS總和×最近3年度平均現金股利發放率 / 審核資料截止日股價'''
    pass



# main functions
def high_div_pool(ticker):
    '''generate a high dividend yield stock pool to make recommendation, ranked by dividend yield'''


def notification_announcement_rebalancing(ticker):
    '''Notifies the announcement of index rebalancing by parsing the PDF file on https://taiwanindex.com.tw/news
    '''