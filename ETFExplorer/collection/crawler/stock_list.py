import pandas as pd
import requests
from bs4 import BeautifulSoup


def crawler(url, CFICode):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml") 
    tr = soup.findAll('tr')

    tds = []
    for raw in tr:
        data = [td.get_text() for td in raw.findAll("td")]
        if len(data) == 7:
            tds.append(data)

    twse_listed = pd.DataFrame(tds[1:],columns=tds[0])
    con_filter = twse_listed['CFICode']==CFICode
    twse_listed = twse_listed[con_filter]
    twse_listed['code'] = twse_listed['有價證券代號及名稱 '].str.extract(r'(\d+)')

    return twse_listed

def get_twse():
    # 獲取上市公司列表
    url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2" 
    return crawler(url, "ESVUFR")

def get_tpex():
    # 獲取上櫃公司列表
    url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4" 
    return crawler(url, "ESVUFR")