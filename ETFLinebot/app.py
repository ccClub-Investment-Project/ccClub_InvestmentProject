from flask import Flask, request, abort
from dotenv import load_dotenv
import logging
import os
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.webhooks.models import MemberJoinedEvent, FollowEvent
from data import *
from message import *
from news2 import *
from stock import *
from consolidate4 import main, main_n


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
    welcome_message = TextMessage(text='歡迎光臨！我是ETF小幫手！\n請輸入"目錄"查找功能')
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
                result3 = historical_stock_message(msg)
                line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result3]))
                user_states[user_id] = None
            elif user_states[user_id] == 'waiting_for_Dividend':
                result4 = main(msg)
                line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result4]))
            elif user_states[user_id] == 'waiting_for_rank':
                result5 = main_n(msg)
                line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result5]))
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
    elif user_state == 'waiting_for_Dividend':
        result4 = main(msg)
        line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result4]))
        user_states[user_id] = None
    elif user_state == 'waiting_for_rank':
        result5 = main_n(msg)
        line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result5]))
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
        message = TextMessage(text="請輸入殖利率")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = 'waiting_for_Dividend'
    elif '最推薦幾股' in msg:
        message = TextMessage(text="請輸入想知道的前幾檔股票")
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
        welcome_message = TextMessage(text='歡迎光臨！我是ETF小幫手！\n請輸入"目錄"查找功能')
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[welcome_message])
        line_bot_api.reply_message(reply_message)


def format_backtest_result(result):
    result_str = str(result)
    start = result_str.find("text='") + 6
    end = result_str.rfind("'")
    content = result_str[start:end]
    formatted_result = content.replace("\\n", "\n")
    return formatted_result

# @handler.add(MemberJoinedEvent)
# def welcome(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         uid = event.joined.members[0].user_id
#         message = TextMessage(text='歡迎光臨!請先key "目錄"')
#         reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
#         line_bot_api.reply_message(reply_message)

@handler.add(FollowEvent)
def handle_follow(event):
    # 發送歡迎訊息
    welcome_message = '歡迎光臨！我是ETF小幫手！\n請輸入"目錄"查找功能'
    message = TextMessage(text=welcome_message)
    user_id = event.source.user_id

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        push_message_request = PushMessageRequest(
            to=user_id,
            messages=[message]
        )
        line_bot_api.push_message(push_message_request)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
