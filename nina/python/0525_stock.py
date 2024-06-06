import requests
from bs4 import BeautifulSoup
import pandas as pd

# 抓取網址
url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb06'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

# 參數
payload = {
    'encodeURIComponent': 1,
    'step': 1, 
    'firstin': 1,
    'off': 1,
    'TYPEK': 'sii',  # 上市公司
    'year': '113',    # 民國年
    'season': '01',   # 季節
}

# 連線抓網頁
res = requests.post(url, headers=headers, data=payload)

# 設定編碼
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

# 確認編碼是否正確解析
test_text = soup.find('table').text  # 確保能夠正確解碼並解析表格內容
if any(char in test_text for char in ['公司', '季']):
    print("解析成功")

# 找到表格
table = soup.find('table', {'class': 'hasBorder'})

if table:
    # 提取每一列數據
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.text.strip() for td in tr.find_all('td')]
        if len(cells) > 0:  # 避免空行
            rows.append(cells)

    print(f"提取到的行數: {len(rows)}")
    if len(rows) > 0:
        print(f"第一行的列數: {len(rows[0])}")

    # 確認提取到的行數據和列數
    for i, row in enumerate(rows[:5]):  # 打印前5行數據作為示例
        print(f"行 {i}: {row}")

    # 確保提取到的數據不為空
    if not rows or not rows[0]:
        print("提取的數據為空。")
    else:
        # 假設表格的第一行是表頭
        headers = rows[0]
        data = rows[1:]

        # 檢查 headers 和 data 是否匹配
        if len(headers) == len(data[0]):
            # 建立DataFrame
            df = pd.DataFrame(data, columns=headers)

            # 將數字轉為數值型態
            for col in df.columns[1:]:  # 跳過第一列，因為它可能不是數字
                df[col] = df[col].str.replace(',', '').apply(pd.to_numeric, errors='coerce')

            # 將DataFrame輸出為CSV
            df.to_csv('financial_data.csv', index=False, encoding='utf-8-sig')
            print("資料已保存為 financial_data.csv")
        else:
            print("表頭數量與行內列數不匹配。")
else:
    print("未找到表格。")





