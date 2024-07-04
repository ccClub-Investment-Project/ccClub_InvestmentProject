

# Calculate dividend
import pandas as pd

# 讀取 CSV 檔案
net_income_df = pd.read_csv('web_scraping_raw_data/processed_filtered_by_net_income.csv', dtype=str)
dividend_df = pd.read_csv('web_scraping_raw_data/processed_financial_dividend_data.csv', dtype=str)

# 將數字列轉換為浮點數以便計算
quarters = ['109季', '110季', '111季', '112季']
for df in [net_income_df, dividend_df]:
    for q in quarters:
        df[q] = df[q].str.replace(',', '').astype(float)

# 計算股利發放率
dividend_df['109股利發放率'] = ((dividend_df['110季'] / net_income_df['109季']) * 100).round(1)
dividend_df['110股利發放率'] = ((dividend_df['111季'] / net_income_df['110季']) * 100).round(1)
dividend_df['111股利發放率'] = ((dividend_df['112季'] / net_income_df['111季']) * 100).round(1)

# 選擇需要的列
result_df = dividend_df[['代號', '公司名稱', '109股利發放率', '110股利發放率', '111股利發放率']]

# 儲存結果到新的 CSV 檔案
result_df.to_csv('web_scraping_raw_data/dividend_payout_ratios.csv', index=False)