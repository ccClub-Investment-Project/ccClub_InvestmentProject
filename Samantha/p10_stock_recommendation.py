import pandas as pd

# 讀取 stock_data_with_dividend_per_share_and_yield.csv 檔案
df = pd.read_csv('web_scraping_raw_data/stock_data_with_dividend_per_share_and_yield.csv')

# 將殖利率轉換為數值，去掉百分比符號並轉換為浮點數
df['dividend_yield'] = df['dividend_yield'].str.rstrip('%').astype(float)

# 選擇殖利率大於 6% 的公司
high_yield_6 = df[df['dividend_yield'] > 6]
high_yield_6 = high_yield_6[['代號', '名稱', 'dividend_yield']]
high_yield_6.sort_values(by='dividend_yield', ascending=False, inplace=True)

# 選擇殖利率大於 5% 的公司
high_yield_5 = df[df['dividend_yield'] > 5]
high_yield_5 = high_yield_5[['代號', '名稱', 'dividend_yield']]
high_yield_5.sort_values(by='dividend_yield', ascending=False, inplace=True)

# 選擇殖利率大於 4% 的公司
high_yield_4 = df[df['dividend_yield'] > 4]
high_yield_4 = high_yield_4[['代號', '名稱', 'dividend_yield']]
high_yield_4.sort_values(by='dividend_yield', ascending=False, inplace=True)

# 將結果合併並去除重複項目
high_yield = pd.concat([high_yield_6, high_yield_5, high_yield_4]).drop_duplicates()

# 排序結果，按照殖利率高到低排列
high_yield.sort_values(by='dividend_yield', ascending=False, inplace=True)

# 打印結果
print(f"殖利率超過6%的股票共{high_yield_6.shape[0]}檔:")
for idx, row in high_yield_6.iterrows():
    print(f"{row['代號']} {row['名稱']} {row['dividend_yield']}")

print(f"\n殖利率超過5%的股票共{high_yield_5.shape[0]}檔:")
for idx, row in high_yield_5.iterrows():
    print(f"{row['代號']} {row['名稱']} {row['dividend_yield']}")

print(f"\n殖利率超過4%的股票共{high_yield_4.shape[0]}檔:")
for idx, row in high_yield_4.iterrows():
    print(f"{row['代號']} {row['名稱']} {row['dividend_yield']}")

# 將結果存儲為新的 CSV 檔案
high_yield.to_csv('web_scraping_raw_data/high_yield_stock_recommendation.csv', index=False)
