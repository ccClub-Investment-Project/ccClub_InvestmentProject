# 加入專案目錄 => 為了讀取別的資料夾
import os
import sys
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_path, '..')
sys.path.insert(0, project_root)
os.chdir(project_root)

from linebot import news

from flask import Flask, request, jsonify
from flasgger import Swagger,swag_from
from dotenv import load_dotenv
load_dotenv()
import os, json

from backtest_manager import BacktestManager
from data import get_json
app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
@swag_from('swagger/home.yaml', methods=['GET'])
def home():
    return "Backtest Running!!!"

@app.route('/one_stock', methods=['GET'])
@swag_from('swagger/one_stock.yaml', methods=['GET'])
def one_stock():
    backtest = BacktestManager()
    # Default values
    id = '0050'
    amount = 3000 
    date = 5
    duration = 10

    if 'id' in request.args:
        id = request.args.get('id')
    if 'amount' in request.args:
        amount = int(request.args.get('amount'))
    if 'date' in request.args:
        date = int(request.args.get('date'))
    if 'duration' in request.args:
        duration = int(request.args.get('duration'))

    stock_ids = [f"{id}.TW"]
    buy_amount = [amount]
    buy_date = date
    duration_year = duration

    try:
        backtest.load_data_yahoo(stock_ids=stock_ids, duration_year=duration_year)
        info = backtest.buy_period(buy_amount, buy_date)
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


@app.route('/etf_all_info', methods=['GET'])
@swag_from('swagger/etf_all_info.yaml', methods=['GET'])
def etf_all_info():
    table = "etf_all_info"
    data = get_json(table)
    return jsonify(data)


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

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5555))
    app.run(host='0.0.0.0', port=port)
