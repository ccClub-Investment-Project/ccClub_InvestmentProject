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
    keyword = 'etf'
    amount = 20 

    if 'keyword' in request.args:
        keyword = request.args.get('keyword')
    if 'amount' in request.args:
        amount = int(request.args.get('amount'))

    new_news = news.CnyesNewsSpider()
    all_news = new_news.get_latest_news()
    filtered = new_news.filter_news(all_news, keyword)
    if len(filtered) >= amount:
        limit = amount
    else: 
        limit = len(filtered)
    filtered_limit = filtered[:limit]
    return jsonify(filtered_limit)


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5555))
    app.run(host='0.0.0.0', port=port)
