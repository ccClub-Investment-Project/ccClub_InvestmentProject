import twstock
from linebot.v3.messaging import TextMessage
from datetime import datetime
import logging

def get_stock_price(stock_code):
    stock = twstock.realtime.get(stock_code)
    if stock['success']:
        return stock['realtime']['open'], stock['realtime']['latest_trade_price']
    message = TextMessage(text="Failed to retrieve data for stock code: {stock_code}")
    return message

def create_stock_message(stock_code):
    open_price, close_price = get_stock_price(stock_code)
    if open_price and close_price:
        send_text = f"Stock Code: {stock_code}\n"
        send_text += f"Open Price: {open_price}\n"
        send_text += f"Close Price: {close_price}"
        message = TextMessage(text=send_text)
    else:
        send_text = "Failed to retrieve stock prices."
        message = TextMessage(text=send_text)
    return message

"""歷史股價查詢"""

def parse_input(input_string):
    parts = input_string.split(',')
    if len(parts) != 3:
        raise ValueError("Input string must contain exactly three parts separated by commas.")
    
    stock_code = parts[0].strip()
    start_date = datetime.strptime(parts[1].strip(), "%Y%m%d")
    end_date = datetime.strptime(parts[2].strip(), "%Y%m%d")
    
    return stock_code, start_date, end_date

def get_historical_stock_prices(stock_code, start_date, end_date):
    import twstock
    stock = twstock.Stock(stock_code)
    historical_data = stock.fetch_from(start_date.year, start_date.month)
    prices = [(d.date, d.open, d.close) for d in historical_data if start_date <= d.date <= end_date]
    return prices

def historical_stock_message(input_string):
    try:
        logging.info(f"Parsing input: {input_string}")
        stock_code, start_date, end_date = parse_input(input_string)
        logging.info(f"Fetching historical prices for {stock_code} from {start_date} to {end_date}")
        historical_prices = get_historical_stock_prices(stock_code, start_date, end_date)
        if historical_prices:
            send_text = f"Stock Code: {stock_code}\nHistorical Prices:\n"
            for date, open_price, close_price in historical_prices:
                send_text += f"Date: {date}, Open: {open_price}, Close: {close_price}\n"
            message = TextMessage(text=send_text)
        else:
            send_text = "No historical stock prices found for the given date range."
            message = TextMessage(text=send_text)
    except Exception as e:
        logging.error(f"Error in historical_stock_message: {e}")
        send_text = f"Failed to retrieve stock prices. Error: {str(e)}"
        message = TextMessage(text=send_text)
    return message


