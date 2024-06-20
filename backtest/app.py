from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from dotenv import load_dotenv
load_dotenv()
import os

from backtest_manager import BacktestManager

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
@swag_from('swagger.yaml', methods=['GET'])
def home():
    return "Backtest Running!!!"

@app.route('/one_stock', methods=['GET'])
@swag_from('swagger.yaml', methods=['GET'], endpoint='one_stock')
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

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5555))
    app.run(host='0.0.0.0', port=port)
