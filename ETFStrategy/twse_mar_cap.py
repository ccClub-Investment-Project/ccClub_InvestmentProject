import requests
import pandas as pd
from bs4 import BeautifulSoup

# 目標網頁 URL
url = 'https://www.taifex.com.tw/cht/9/futuresQADetail'

# 發送 GET 請求
response = requests.get(url)

# 檢查回應是否成功
if response.status_code != 200:
    print(f"Failed to retrieve page: {response.status_code}")
    exit()

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 找到目標表格
table = soup.find('table', class_='table_a')

# 檢查表格是否找到
if table is None:
    print("Table not found")
    exit()

# 提取表格內容
data = []
for tr in table.find_all('tr'):
    row = []
    for td in tr.find_all('td'):
        row.append(td.text.strip())
    if row:
        data.append(row)

# 提取特定欄位資料
formatted_data = []
for row in data:
    if len(row) >= 3:  # 確保每一行至少有三個欄位
        security_name = row[0]
        market_value_ratio = row[1]
        market_ratio = row[2]
        formatted_data.append([security_name, market_value_ratio, market_ratio])

# 將資料轉成 DataFrame
df = pd.DataFrame(formatted_data, columns=['證券名稱', '市值佔大盤比重', '大盤比重'])

# 儲存成 CSV 檔案
df.to_csv('taifex_futures_qa.csv', index=False, encoding='utf-8-sig')

print("CSV file 'taifex_futures_qa.csv' has been saved successfully.")
