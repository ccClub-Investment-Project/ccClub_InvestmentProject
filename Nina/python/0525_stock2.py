import requests
from bs4 import BeautifulSoup as bs
from io import StringIO
import pandas as pd

# 抓取網址
url = 'https://mops.twse.com.tw/mops/web/t108sb27'

# 參數
payload = {
    'encodeURIComponent': 1,
    'step': 1,
    'firstin': 1,
    'off': 1,
    'TYPE': 'sil',
    'year': '113',
    "keyword4": "",
    "code1": "",
    "TYPEK2": "",
    "checkbtn": "",
    "queryName": "",
    "co_id_1": "",
    "co_id_2": "",
    "month": "",
    "b_date": "",
    "e_date": "",
    "type": "",
}

# 發送初始請求以獲取隱藏輸入字段
res = requests.get(url, params=payload)
soup = bs(res.text, 'lxml')

# 提取隱藏字段的值
inp = soup.select("input[type=hidden]")
if not inp:
    raise ValueError("未找到隱藏輸入字段。")

# 構建新的請求負載
ur1 = 'https://mops.twse.com.tw/server-java/t105sb02'
payload = {
    'firstin': "true",
    "step": 10,
    'filename': inp[-1]["value"]
}

# 發送新請求以獲取CSV數據
res = requests.get(ur1, params=payload)

# 嘗試不同的編碼以確保正確解析
encodings = ['utf-8']
soup = None
for encoding in encodings:
    res.encoding = encoding
    soup = bs(res.text, 'html.parser')
    test_text = soup.text  # 確保能夠正確解碼並解析表格內容
    if any(char in test_text for char in ['公司', '季']):
        print(f"使用編碼 {encoding} 解析成功")
        break
else:
    raise ValueError("無法使用任何編碼正確解析內容。")

# 提取CSV數據並讀取到DataFrame
df3 = pd.read_csv(StringIO(res.text), delimiter=',', on_bad_lines='warn')
print(df3)
