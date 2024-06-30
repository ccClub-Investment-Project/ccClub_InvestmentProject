from flask import Flask, request, abort
from dotenv import load_dotenv
import logging
import os
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.webhooks.models import MemberJoinedEvent
from data import *
from message import *
from news2 import *
from stock import *

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Samantha'))
from Samantha import filter_stocks, filter_top_10_dividend_stocks


# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load environment variables
channel_access_token = os.getenv('channel_access_token')
channel_secret = os.getenv('channel_secret')
port = int(os.getenv('PORT', 5000))

# Get instance from linebot
configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

user_states = {}
user_inputs = {}

@app.route("/")
def home():
    return "Webhook Running!!!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    line_bot_api = MessagingApi(ApiClient(configuration))
    user_id = event.source.user_id
    msg = event.message.text.strip()
    logging.info(f"Received message: {msg} from user: {user_id} with reply token: {event.reply_token}")

    # 默认回复消息
    welcome_message = TextMessage(text='歡迎光臨!請先key "目錄"')
    line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[welcome_message]))

    try:
        if user_id in user_states:
            if user_states[user_id] == 'waiting_for_keywords':
                handle_keywords_input(line_bot_api, event, msg, user_id)
            elif user_states[user_id] == 'waiting_for_stock':
                result2 = create_stock_message(msg)
                line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result2]))
                user_states[user_id] = None
            elif user_states[user_id] == 'waiting_for_backtest':
                result1 = backtest(msg)
                formatted_result = format_backtest_result(result1)
                line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=formatted_result)]))
                user_states[user_id] = None
            elif user_states[user_id] == 'waiting_for_hstocks':
                logging.info(f"Processing historical stock message for {msg}")
                result3 = historical_stock_message(msg)
                line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result3]))
                user_states[user_id] = None


            elif user_state == 'waiting_for_Dividend':
                if msg == '1':
                    user_states[user_id] = 'waiting_for_Dividend_Simple'
                    message = TextMessage(text="請選擇股市小白還是股市高手？\n1. 股市小白\n2. 股市高手")
                    line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[message]))
                elif msg == '2':
                    user_states[user_id] = 'waiting_for_Dividend_Advanced'
                    message = TextMessage(
                        text="請輸入市值(億), 交易量(億), 是否前一年獲利(Y/N), 是否連續三年發放現金股利(Y/N), 現金殖利率 (%) \n例如：1000, 10, Y, Y, 3.0")
                    line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[message]))
                else:
                    message = TextMessage(text="請選擇「1」或「2」")
                    line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[message]))
            elif user_state == 'waiting_for_Dividend_Simple':
                if msg == '1':
                    # 取得殖利率最高的十檔股票
                    top_10_stocks = filter_top_10_dividend_stocks()
                    if top_10_stocks:
                        message_text = "以下是殖利率最高的十檔股票：\n"
                        for stock in top_10_stocks:
                            message_text += f"{stock['代號']} - {stock['名稱']} 現金殖利率: {float(stock['現金殖利率']) * 100:.2f}%\n"
                        line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token,
                                                                       messages=[TextMessage(text=message_text)]))
                    else:
                        line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[
                            TextMessage(text="無法取得殖利率最高的股票資料。")]))
                else:
                    message = TextMessage(text="請輸入「1」來查看殖利率最高的十檔股票")
                    line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[message]))

            elif user_state == 'waiting_for_Dividend_Advanced':
                try:
                    min_market_cap, min_trading_volume, profit_or_not, payout, dividend_yield = [x.strip() for x in
                                                                                                 msg.split(',')]
                    min_market_cap = float(min_market_cap)
                    min_trading_volume = float(min_trading_volume)
                    dividend_yield = float(dividend_yield)

                    # 執行選股邏輯
                    stocks = filter_stocks(min_market_cap, min_trading_volume, profit_or_not, payout, dividend_yield)
                    if stocks:
                        message = "\n".join(
                            [f"{stock['代號']} - {stock['名稱']} 現金殖利率: {float(stock['現金殖利率']) * 100:.2f}%"
                             for stock in stocks])
                    else:
                        message = "沒有符合條件的股票。"

                    line_bot_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=message)]))


                except Exception as e:
                    logging.error(f"Error in dividend filtering: {e}")
                    line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[
                        TextMessage(text="輸入的參數有誤，請重新檢查格式。")]))
                user_states[user_id] = None


            else:
                handle_regular_message(line_bot_api, event, msg, user_id)
        else:
            handle_regular_message(line_bot_api, event, msg, user_id)
    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        error_message = TextMessage(text="發生錯誤，請稍後再試。")
        line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[error_message]))
        user_states[user_id] = None

def handle_keywords_input(line_bot_api, event, msg, user_id):
    keywords = [keyword.strip() for keyword in msg.split(',') if keyword.strip()]
    if keywords:
        logging.info(f"Fetching news for keywords: {keywords}")
        message = fetch_and_filter_news_message(keywords, limit=10)

        if isinstance(message, TextMessage):
            logging.info(f"Fetched news: {message.text[:100]}...")  # Log first 100 chars of the text
            reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        else:
            message_str = str(message)
            logging.info(f"Fetched news: {message_str[:100]}...")  # Log first 100 chars
            reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=message_str)])

        line_bot_api.reply_message(reply_message)
    else:
        prompt_message = TextMessage(text="請輸入有效的關鍵字，用逗號分隔:")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[prompt_message])
        line_bot_api.reply_message(reply_message)
    user_states[user_id] = None  # 重置用戶狀態

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    line_bot_api = MessagingApi(ApiClient(configuration))
    user_id = event.source.user_id
    msg = event.message.text.strip()
    logging.info(f"Received message: {msg} from user: {user_id} with reply token: {event.reply_token}")

    # Check if the user is in a specific state
    user_state = user_states.get(user_id)

    if user_state == 'waiting_for_keywords':
        handle_keywords_input(line_bot_api, event, msg, user_id)
    elif user_state == 'waiting_for_stock':
        result2 = create_stock_message(msg)
        line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result2]))
        user_states[user_id] = None
    elif user_state == 'waiting_for_backtest':
        result1 = backtest(msg)
        formatted_result = format_backtest_result(result1)
        line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=formatted_result)]))
        user_states[user_id] = None
    elif user_state == 'waiting_for_hstocks':
        result3 = historical_stock_message(msg)
        line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result3]))
        user_states[user_id] = None
    else:
        handle_regular_message(line_bot_api, event, msg, user_id)

def handle_regular_message(line_bot_api, event, msg, user_id):
    if "歷史股價查詢" in msg:
        message = TextMessage(text="請輸入公司代號,開始日期,結束日期(請用半形逗號隔開)例如,0050,20240608,20240628):")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = 'waiting_for_hstocks'
    elif '換股' in msg:
        message = buttons_message()
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
    elif '殖利率篩選' in msg:
        message = buttons_message()
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = 'waiting_for_Dividend'
    elif '最推薦幾股' in msg:
        message = buttons_message()
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = 'waiting_for_rank'
    elif '目錄' in msg:
        carousel = Carousel_Template()
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[carousel])
        line_bot_api.reply_message(reply_message)
    elif '新聞' in msg:
        message = TextMessage(text="請輸入關鍵字，用半形逗號分隔:")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = 'waiting_for_keywords'
    elif '即時開盤價跟收盤價' in msg:
        message = TextMessage(text="請輸入股票代號:")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = 'waiting_for_stock'
    elif '回測' in msg:
        message = TextMessage(text="輸入股票代號與定期定額金額(半形逗號隔開):例如,0050,6000")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = 'waiting_for_backtest'
    else:
        welcome_message = TextMessage(text='歡迎光臨!請先key "目錄"')
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[welcome_message])
        line_bot_api.reply_message(reply_message)





def format_backtest_result(result):
    result_str = str(result)
    start = result_str.find("text='") + 6
    end = result_str.rfind("'")
    content = result_str[start:end]
    formatted_result = content.replace("\\n", "\n")
    return formatted_result

@handler.add(MemberJoinedEvent)
def welcome(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        uid = event.joined.members[0].user_id
        gid = event.source.group_id
        profile = line_bot_api.get_group_member_profile(gid, uid)
        name = profile.display_name
        message = TextMessage(text=f'歡迎光臨!請先key "目錄"')
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)

# 選股



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
