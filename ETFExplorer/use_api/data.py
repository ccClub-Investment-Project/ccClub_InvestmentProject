import requests
import yfinance


url_base = "https://backtest-kk2m.onrender.com"
url_table = 'https://backtest-kk2m.onrender.com/tables'

def get_stock_data(id, amount=6000):
    url = 'https://backtest-kk2m.onrender.com/backtest/{id}'.format(id=id)
    params = {
        'amount': amount,
    }
    response = requests.get(url, params=params)
    return response.json()

def get_news_data(keywords, etf, limit):
    url = url_base + "/news"
    params = {
        'keywords': keywords,
        'etf': etf,
        'limit': limit
    }
    response = requests.get(url, params=params)
    return response.json()


def api_table_data(table_name):
    url = url_table + "/" + table_name
    response = requests.get(url)
    data = response.json()
    return data


# news = get_news_data('台股,美股',True, 25)
# print(len(news))
# print(news[0])

# https://news.cnyes.com/news/id/{news['newsId']