

'''average_turnover csv檔中，成交金額單位為元'''


# Part 2: liquidity check:
'''Liquidity check: the average daily trading volume reaches 100 million 每日平均成交額達1億'''




import pandas as pd

# 輸入和輸出 CSV 文件路徑
input_csv_file = 'web_scraping_raw_data/average_turnovers.csv'
output_csv_file = 'web_scraping_raw_data/filtered_average_turnovers.csv'

# 讀取 CSV 文件
df = pd.read_csv(input_csv_file)

# 過濾掉 average_turnover 小於 100,000,000 的股票
filtered_df = df[df['average_turnover'] >= 100000000]

# 將過濾後的數據輸出為 CSV 文件
filtered_df.to_csv(output_csv_file, index=False)

print("完成過濾並輸出到新的 CSV 文件。")
