import pandas as pd
import requests
import io

url = 'https://mops.twse.com.tw/server-java/FileDownLoad'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/111.25 (KHTML, like Gecko) Chrome/99.0.2345.81 Safari/123.36'}
payload = {
    'step': '9',
    'functionName': 'show_file2',
    'filePath': '/t21/sii/', # otc
    'fileName': 't21sc03_110_1.csv'
}

res = requests.post(url,data=payload,headers=headers)

res.encoding = 'utf8'
df = pd.read_csv(io.StringIO(res.text))
# 將不必要的符號去除
df = df.map(lambda s:str(s).replace(',','')).set_index('公司代號')
# 將數字轉為數值型態
df = df.map(lambda s:pd.to_numeric(str(s),errors='coerce')).dropna(how='all',axis=1)
print(df)