import requests

url_base = 'https://backtest-kk2m.onrender.com'

def get_stock_data(id, amount, duration):
    url = url_base + "/one_stock"
    params = {
        'id': id,
        'amount': amount,
        'duration': duration
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

# news = get_news_data('台股,美股',True, 25)
# print(len(news))
# print(news[0])

# https://news.cnyes.com/news/id/{news['newsId']