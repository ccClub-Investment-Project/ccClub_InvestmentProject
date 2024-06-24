import pandas as pd

# 讀取原始CSV文件
input_csv_file = 'web_scraping_raw_data/f_data.csv'
df = pd.read_csv(input_csv_file)

# 讀取包含股票代號的CSV文件，並指定名稱和代號欄位
ticker_file = 'web_scraping_raw_data/top_mar_cap_companies.csv'
df_ticker = pd.read_csv(ticker_file, usecols=['代號', '名稱'])

# 將「名稱」改名為「公司名稱」，以便後續合併
df_ticker.rename(columns={'名稱': '公司名稱'}, inplace=True)

# 去掉 id 欄位，並將 公司名稱 欄位移到最左邊
df = df.drop(columns=['id'])
df = df[['公司名稱', '季度', '營業利益損失', '母公司業主淨利損']]

# 將帶逗號的數字轉換為數值類型
df['營業利益損失'] = df['營業利益損失'].str.replace(',', '').astype(float)
df['母公司業主淨利損'] = df['母公司業主淨利損'].str.replace(',', '').astype(float)

# 檢查重複的項目
duplicate_rows = df[df.duplicated(subset=['公司名稱', '季度'], keep=False)]

# 若存在重複項目，這裡先將它們的營業利益損失和母公司業主淨利損合併為平均值
if not duplicate_rows.empty:
    df = df.groupby(['公司名稱', '季度'], as_index=False).mean()

# 設定季度標籤順序
quarter_labels = [
    "2023 第一季", "2023 第二季", "2023 第三季", "2023 第四季",
    "2024 第一季"
]

# 與股票代號的數據合併，根據 公司名稱
df_merged = pd.merge(df, df_ticker, on='公司名稱', how='left')

# 分別創建兩個 DataFrame，用於存儲 營業利益損失 和 母公司業主淨利損
df_operating_income = df_merged.pivot(index=['代號', '公司名稱'], columns='季度', values='營業利益損失').reindex(columns=quarter_labels).reset_index()
df_net_income = df_merged.pivot(index=['代號', '公司名稱'], columns='季度', values='母公司業主淨利損').reindex(columns=quarter_labels).reset_index()

# 存儲為CSV文件
output_operating_income_file = 'web_scraping_raw_data/operating_income.csv'
output_net_income_file = 'web_scraping_raw_data/net_income.csv'

df_operating_income.to_csv(output_operating_income_file, index=False)
df_net_income.to_csv(output_net_income_file, index=False)

print("已完成重新格式化並儲存為兩個CSV文件。")
