# 加入專案目錄 => 為了讀取別的資料夾
import os
import sys
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_path, '..')

# 将 ETFLinebot 文件夹添加到系统路径
etflinebot_path = os.path.join(project_root, 'ETFLinebot')
print(etflinebot_path)
sys.path.append(etflinebot_path)

etfexplorer_path = os.path.join(project_root, 'ETFExplorer')
print(etfexplorer_path)
sys.path.append(etfexplorer_path)

import news, consolidate3

from flask import Flask, request, jsonify
from flasgger import Swagger,swag_from
from dotenv import load_dotenv
load_dotenv()
import os, json

from backtest_manager import BacktestManager
from data import get_json

from app_tools.pickle_handler import load_data

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
@swag_from('swagger/home.yaml', methods=['GET'])
def home():
    return "Backtest Running!!!"

@app.route('/backtest/<stock_id>', methods=['GET'])
@swag_from('swagger/backtest_stock.yaml', methods=['GET'])
def backtest_stock(stock_id):
    backtest = BacktestManager()
    # Default values
    amount = 6000 
    id = stock_id
    if 'amount' in request.args:
        amount = int(request.args.get('amount'))
    
    stock_id = f"{id}.TW"
    buy_amount = amount

    try:
        backtest.load_data_yahoo(stock_id=stock_id)
        info = backtest.buy_period(buy_amount)
        log = backtest.run()
        analysis = backtest.analysis()
    except Exception as e:
        print(f"Error: {e}")
        info = "error"
        analysis = "error"
        log = "error"

    # Prepare response
    response = {
        'id': id,
        'info': info,
        'analysis': analysis,
        'log': log
    }
    return jsonify(response)

@app.route('/news',methods=['GET'])
@swag_from('swagger/news.yaml', methods=['GET'])
def get_news():
    # Default values
    keywords = '台股,美股'
    limit = 25
    etf = True

    if 'keywords' in request.args:
        keywords = request.args.get('keywords')
    if 'etf' in request.args:
        etf = bool(request.args.get('etf'))
    if 'limit' in request.args:
        limit = int(request.args.get('limit'))

    new_news = news.CnyesNewsSpider()
    all_news = new_news.get_latest_news()
    
    filtered = []

    # 設定ETF filter
    def get_etf_filter(etf,all_news):
        etf_list=[]
        if etf == True:
            for new in all_news:
                if new['etf']!=[]:
                    etf_list.append(new)
        return etf_list

    # 設定keyword filter
    def get_keyword_filter(keywords, all_news):
        keywords_list=[]
        for new in all_news:
            # match in keyword array
            if any(keyword in new.get("keyword") for keyword in keywords):
                keywords_list.append(new)
            # match in title
            if any(keyword.lower() in new.get("title", "").lower() for keyword in keywords):
                keywords_list.append(new)
        return keywords_list

    etf_list = get_etf_filter(etf, all_news)
    keywords_list = get_keyword_filter(keywords, all_news)

    # 合并 ETF 和关键词过滤后的列表
    combined_list = etf_list + keywords_list

    # 移除重复的 newsId
    unique_news = []
    seen_news_ids = set()
    for news_item in combined_list:
        news_id = news_item['newsId']
        if news_id not in seen_news_ids:
            unique_news.append(news_item)
            seen_news_ids.add(news_id)

    # 限制返回的结果数量
    filtered = unique_news[:limit]

    return jsonify(filtered)

@app.route('/tables/<table_name>', methods=['GET'])
@swag_from('swagger/tables.yaml', methods=['GET'])
def etf_all_info(table_name):
    data = get_json(table_name)
    return jsonify(data)

@app.route('/strategy/basic', methods=['GET'])
@swag_from('swagger/strategy_basic.yaml', methods=['GET'])
def get_strategy_basic():
    top_n = 0
    if 'top_n' in request.args:
        top_n = int(request.args.get('top_n'))

    df = consolidate3.strategy_basic(top_n).df_filtered
    df = df[['代號', '名稱', '現金殖利率']]
    if df.empty:
        return jsonify({"message": "没有符合条件的股票。"})

    return jsonify(df.to_dict(orient='records'))

@app.route('/strategy/yield', methods=['GET'])
@swag_from('swagger/strategy_yield.yaml', methods=['GET'])
def get_strategy_yield():
    min_yield = 5
    if 'min_yield' in request.args:
        min_yield = float(request.args.get('min_yield'))

    df = consolidate3.strategy_yield(min_yield).df_filtered
    df = df[['代號', '名稱', '現金殖利率']]
    if df.empty:
        return jsonify({"message": "没有符合条件的股票。"})

    return jsonify(df.to_dict(orient='records'))

@app.route('/all_etf_history',methods=['GET'])
def get_all_etf_history():
    data = load_data("all_etf_history")
    code = request.args.get('code')

    if code:
        if code in data:
            df = data[code]
            return jsonify(df.to_dict(orient='records'))
        else:
            return jsonify({"error": f"Data for {code} not found"}), 404
    else:
        # 如果未提供 etf_code，返回所有數據
        data_dict = {key: df.to_dict(orient='records') for key, df in data.items()}
        return jsonify(data_dict)


@app.route('/all_etf_code', methods=['GET'])
def get_all_etf_code():
    data = load_data("all_etf_code")
    return jsonify(data)


@app.route('/all_history',methods=['GET'])
def get_all_history():
    data = load_data("all_history")
    code = request.args.get('code')

    if code:
        if code in data:
            df = data[code]
            return jsonify(df.to_dict(orient='records'))
        else:
            return jsonify({"error": f"Data for {code} not found"}), 404
    else:
        # 如果未提供 etf_code，返回所有數據
        data_dict = {key: df.to_dict(orient='records') for key, df in data.items()}
        return jsonify(data_dict)

@app.route('/all_code', methods=['GET'])
def get_all_code():
    data = load_data("all_code")
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5555))
    app.run(host='0.0.0.0', port=port)
