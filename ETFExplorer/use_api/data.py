import requests
import yfinance

URL_BASE = "https://backtest-kk2m.onrender.com"
URL_TABLE = f"{URL_BASE}/tables"
URL_Strategy = f"{URL_BASE}/strategy"

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
    max_retries = 2 
    retries = 0
    while retries <= max_retries:
        try:
            response = session.get(url, params=params, timeout=300)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching news data: {e}")
            retries += 1
            if retries <= max_retries:
                print(f"Retrying ({retries}/{max_retries})...")
                time.sleep(1)  # 等待1秒後重試
            else:
                print(f"Max retries exceeded. Returning empty list.")
                return []

def api_table_data(table_name):
    url = f"{URL_TABLE}/{table_name}"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching table data: {e}")
        return None

def get_strategy_basic(top_n=0):
    url = f"{URL_Strategy}/basic"
    params = {'top_n': top_n}

    try:
        response = session.get(url,params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching table data: {e}")
        return None

def get_strategy_yield(min_yield=5):
    params = {'min_yield': min_yield}

    url = f"{URL_Strategy}/yield"
    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching table data: {e}")
        return None




# test = api_table_data("etf_performance")
# print(test[0])
# news = get_news_data('台股,美股',True, 25)
# print(len(news))
# print(news[0])

# https://news.cnyes.com/news/id/{news['newsId']


# test = get_strategy_basic(20)
# test = get_strategy_yield(1)
# print (len(test))