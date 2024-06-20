from flask import Flask, request, abort
from dotenv import load_dotenv
import logging
import os
import tempfile
import datetime
import time
from data import backtest
import re
from linebot.v3 import WebhookHandler
from linebot import LineBotApi
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (Configuration,ApiClient,MessagingApi,ReplyMessageRequest,TextMessage)
from linebot.v3.webhooks import (MessageEvent,TextMessageContent)
from linebot.v3.webhooks.models import MemberJoinedEvent
load_dotenv()


# save loggings
current_directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_directory, 'logs/linebot.log')

# logging setting
logging.basicConfig(
    level=logging.DEBUG,  # debug
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # format
    handlers=[
        # logging.FileHandler(log_file_path),  # export file
        logging.StreamHandler()  # export console
    ]
)

# Custom module imports
from message import *
from news import *
from Function import *

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# Load environment variables
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('CHANNEL_SECRET')
port = int(os.getenv('PORT', 5000))

# get instance from linbot
configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

user_states = {}

@app.route("/")
def home():
    return "Webhook Running!!!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        user_id = event.source.user_id
        msg = event.message.text.strip()
        logging.info(f"Received message: {msg} from user: {user_id} with reply token: {event.reply_token}")

        try:
            if user_id in user_states and user_states[user_id] == 'waiting_for_keywords':
                handle_keywords_input(line_bot_api ,event, msg, user_id)
            else:
                handle_regular_message(line_bot_api, event, msg, user_id)
        except Exception as e:
            logging.error(f"Error handling webhook: {e}")
            error_message = TextMessage(text="發生錯誤，請稍後再試。")
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[error_message]
                )
            )
            user_states[user_id] = None


def handle_keywords_input(line_bot_api, event, msg, user_id):
    try:
        keywords = [keyword.strip() for keyword in msg.split(',') if keyword.strip()]
        if keywords:
            message = fetch_and_filter_news_message(keywords, limit=10)
            line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[message]
                )
            )
        else:
            prompt_message = TextMessage(text="請輸入有效的關鍵字，用逗號分隔:")
            line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[message]
                )
            )
            # line_bot_api.reply_message(event.reply_token, prompt_message)
    except Exception as e:
        logging.error(f"Error in handle_keywords_input: {e}")
    finally:
        user_states[user_id] = None



user_states = {}  # 用来存储用户状态的字典

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = LineBotApi(api_client)

        user_id = event.source.user_id
        msg = event.message.text.strip()
        logging.info(f"Received message: {msg} from user: {user_id} with reply token: {event.reply_token}")

        try:
            if user_id in user_states and user_states[user_id] == 'waiting_for_keywords':
                handle_keywords_input(line_bot_api, event, msg, user_id)
            else:
                handle_regular_message(line_bot_api, event, msg, user_id)
        except Exception as e:
            logging.error(f"Error handling webhook: {e}")
            error_message = TextMessage(text="發生錯誤，請稍後再試。")
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[error_message]
                )
            )
            user_states[user_id] = None


def handle_keywords_input(line_bot_api, event, msg, user_id):
    try:
        keywords = [keyword.strip() for keyword in msg.split(',') if keyword.strip()]
        if keywords:
            message = fetch_and_filter_news_message(keywords, limit=10)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TextMessage(text=message)]
                )
            )
        else:
            prompt_message = TextMessage(text="請輸入有效的關鍵字，用逗號分隔:")
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[prompt_message]
                )
            )
    except Exception as e:
        logging.error(f"Error in handle_keywords_input: {e}")
    finally:
        user_states[user_id] = None

user_states = {}  # 用来存储用户状态的字典

from linebot.v3.messaging import LineBotApi  # Ensure LineBotApi is imported

# Correct handle_message function
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        line_bot_api = LineBotApi(channel_access_token)  # Use LineBotApi directly with the access token

        user_id = event.source.user_id
        msg = event.message.text.strip()
        logging.info(f"Received message: {msg} from user: {user_id} with reply token: {event.reply_token}")

        if user_id in user_states and user_states[user_id] == 'waiting_for_keywords':
            handle_keywords_input(line_bot_api, event, msg, user_id)
        else:
            handle_regular_message(line_bot_api, event, msg, user_id)
    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        error_message = TextMessage(text="發生錯誤，請稍後再試。")
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[error_message]
            )
        )
        user_states[user_id] = None


def handle_keywords_input(line_bot_api, event, msg, user_id):
    try:
        keywords = [keyword.strip() for keyword in msg.split(',') if keyword.strip()]
        if keywords:
            message = fetch_and_filter_news_message(keywords, limit=10)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TextMessage(text=message)]
                )
            )
        else:
            prompt_message = TextMessage(text="請輸入有效的關鍵字，用逗號分隔:")
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[prompt_message]
                )
            )
    except Exception as e:
        logging.error(f"Error in handle_keywords_input: {e}")
    finally:
        user_states[user_id] = None

def handle_regular_message(line_bot_api, event, msg, user_id):
    try:
        if '財報' in msg:
            message = buttons_message1()
        elif '基本股票功能' in msg:
            message = buttons_message1()
        elif '換股' in msg:
            message = buttons_message2()
        elif '目錄' in msg:
            message = Carousel_Template()
        elif '新聞' in msg:
            message = TextMessage(text="請輸入關鍵字，用逗號分隔:")
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[message]
                )
            )
            user_states[user_id] = 'waiting_for_keywords'
            return
        elif '功能列表' in msg:
            message = function_list()
        elif '回測' in msg:
            message = TextMessage(text="請問要回測哪一支,定期定額多少,幾年(請用逗號隔開):")
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[message]
                )
            )
            user_states[user_id] = 'waiting_for_backtest'
            return

        if user_states.get(user_id) == 'waiting_for_backtest':
            try:
                logging.info(f"收到回測輸入: {msg}")  # 调试信息
                result = backtest(msg)
                logging.info(f"回測結果: {result}")  # 调试信息
                message = TextMessage(text=result)  # 确保 result 是字符串
            except ValueError as e:
                logging.error(f"解析輸入時發生錯誤: {e}")  # 调试信息
                message = TextMessage(text="輸入格式錯誤，請按照 '標的,定期定額,年數' 的格式輸入")
            finally:
                user_states[user_id] = None  # 重置狀態
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[message]
                )
            )
            return

        # 如果没有命中任何条件，提供默认回复
        else:
            message = TextMessage(text="未知的指令，請輸入有效的指令")

        # 默认情况下回复消息
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[message]
            )
        )
    except Exception as e:
        logging.error(f"處理訊息時發生錯誤: {e}")  # 调试信息
        message = TextMessage(text="發生錯誤，請稍後再試")
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[message]
            )
        )


@handler.add(MemberJoinedEvent)
def welcome(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        uid = event.joined.members[0].user_id
        gid = event.source.group_id
        profile = line_bot_api.get_group_member_profile(gid, uid)
        name = profile.display_name
        message = TextMessage(text=f'{name}歡迎加入')
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[message]
            )
        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)