import requests
import yfinance

URL_BASE = "https://backtest-kk2m.onrender.com"
URL_TABLE = f"{URL_BASE}/tables"

session = requests.Session()

def get_stock_data(id, amount=6000):
    url = f"{URL_BASE}/backtest/{id}"
    params = {'amount': amount}
    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching stock data: {e}")
        return None

def get_news_data(keywords, etf, limit):
    url = f"{URL_BASE}/news"
    params = {'keywords': keywords, 'etf': etf, 'limit': limit}
    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching news data: {e}")
        return None

def api_table_data(table_name):
    url = f"{URL_TABLE}/{table_name}"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching table data: {e}")
        return None


# news = get_news_data('台股,美股',True, 25)
# print(len(news))
# print(news[0])

# https://news.cnyes.com/news/id/{news['newsId']