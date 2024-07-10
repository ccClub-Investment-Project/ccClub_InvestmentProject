import requests
import time
import yfinance as yf
from requests.exceptions import RequestException

# URL_BASE = "https://backtest-kk2m.onrender.com"
URL_BASE = "https://backtest-2.onrender.com"

URL_TABLE = f"{URL_BASE}/tables"
URL_Strategy = f"{URL_BASE}/strategy"

session = requests.Session()


# code: 2330.TW or 6XXX.TWO
# def api_history(code):
#     url = f"{URL_BASE}/all_history"
#     params = {'code': code}
#     try:
#         response = session.get(url,params=params, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         print(f"Error fetching table data: {e}")
#         return None

def api_code():
    url = f"{URL_BASE}/all_code"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching table data: {e}")
        return None
    
# code: 2330.TW or 6XXX.TWO
# def api_etf_history(code):
#     url = f"{URL_BASE}/all_etf_history"
#     params = {'code': code}
#     try:
#         response = session.get(url,params=params, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         print(f"Error fetching table data: {e}")
#         return None

def api_etf_code():
    url = f"{URL_BASE}/all_etf_code"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching table data: {e}")
        return None
    
def fetch_stock_data(stock_id):
    try:
        # print(f"Attempting to fetch data for {stock_id}")
        df = yf.download(stock_id, progress=False)
        
        if df.empty:
            raise ValueError(f"No data retrieved for {stock_id}")
        
        df.reset_index(inplace=True)
        # print(f"Successfully fetched data for {stock_id}")
        return df
    except RequestException as e:
        # print(f"Network error while fetching data for {stock_id}: {e}")
        raise ValueError(f"Network error: {e}")
    except Exception as e:
        # print(f"Unexpected error while fetching data for {stock_id}: {e}")
        raise ValueError(f"Unexpected error: {e}")

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
        response = session.get(url, params=params, timeout=2000)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching table data: {e}")
        return None

def get_all_plot_data():
    all_yield = get_strategy_yield(0)
    all_data = {}
    
    for stock in all_yield:
        code = int(stock['代號'])
        stock_id = f"{code}.TW"
        
        try:
            df = fetch_stock_data(stock_id)
            all_data[stock_id] = df
            # print(f"Successfully added data for {stock_id} to all_data")
        except ValueError as e:
            # print(f"Error with {stock_id}: {e}")
            stock_id = f"{code}.TWO"
            try:
                df = fetch_stock_data(stock_id)
                all_data[stock_id] = df
                # print(f"Successfully added data for {stock_id} to all_data")
            except ValueError as e:
                pass
                # print(f"Error with {stock_id}: {e}")
                # print(f"Skipping stock {code}")
                continue
    return all_data


# test = api_table_data("etf_performance")
# print(test[0])
# news = get_news_data('台股,美股',True, 25)
# print(len(news))
# print(news[0])

# https://news.cnyes.com/news/id/{news['newsId']


# test = get_strategy_basic(20)
# test = get_strategy_yield(1)
# print (len(test))