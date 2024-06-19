from flask import Flask, request, abort
from dotenv import load_dotenv
import logging
import os
import tempfile
import datetime
import time
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, MemberJoinedEvent, TextSendMessage

load_dotenv()

# Custom module imports
from message import *
from news import *
from Function import *

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# Load environment variables
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

user_states = {}

@app.route("/")
def home():
    return "Webhook Running!!!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        app.logger.error(f"Error handling webhook body: {e}")
        abort(500)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text.strip()

    logging.info(f"Received message: {msg} from user: {user_id} with reply token: {event.reply_token}")

    try:
        if user_id in user_states and user_states[user_id] == 'waiting_for_keywords':
            handle_keywords_input(event, msg, user_id)
        else:
            handle_regular_message(event, msg, user_id)
    except LineBotApiError as e:
        logging.error(f"Error handling webhook: {e}")
        error_message = TextSendMessage(text="發生錯誤，請稍後再試。")
        line_bot_api.reply_message(event.reply_token, error_message)
        user_states[user_id] = None

def handle_keywords_input(event, msg, user_id):
    try:
        keywords = [keyword.strip() for keyword in msg.split(',') if keyword.strip()]
        if keywords:
            message = fetch_and_filter_news_message(keywords, limit=10)
            line_bot_api.reply_message(event.reply_token, message)
        else:
            prompt_message = TextSendMessage(text="請輸入有效的關鍵字，用逗號分隔:")
            line_bot_api.reply_message(event.reply_token, prompt_message)
    except LineBotApiError as e:
        logging.error(f"Error in handle_keywords_input: {e}")
    finally:
        user_states[user_id] = None

def handle_regular_message(event, msg, user_id):
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
            prompt_message = TextSendMessage(text="請輸入關鍵字，用逗號分隔:")
            line_bot_api.reply_message(event.reply_token, prompt_message)
            user_states[user_id] = 'waiting_for_keywords'
            return
        elif '功能列表' in msg:
            message = function_list()
        else:
            message = TextSendMessage(text=msg)
        
        line_bot_api.reply_message(event.reply_token, message)
    except LineBotApiError as e:
        logging.error(f"Error in handle_regular_message: {e}")
        error_message = TextSendMessage(text="發生錯誤，請稍後再試。")
        line_bot_api.reply_message(event.reply_token, error_message)
        user_states[user_id] = None

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
