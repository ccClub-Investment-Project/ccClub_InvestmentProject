from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from news import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('yXUDkIIyLEoIuWSiKdrJ7EcgUrq05cpRd/Mh7+xFfznOYE6aNmeiC7SARxkey8fZ3hBOROk8pPMP6c3HBjDRAoQCMF9o3bzAENnOCeQtaB98c4YnE3qVIxEPuRXhTD2pNX1d/J83SwjK/GCEHtMsPwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e173edcacc6b33a6c041d95bcf1a6198')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        app.logger.error(f"Error handling webhook body: {e}")
        abort(500)

    return 'OK'

import logging
from linebot.exceptions import LineBotApiError

user_states = {}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text.strip()
    
    logging.info(f"Received message: {msg} from user: {user_id} with reply token: {event.reply_token}")

    try:
        # Check user state
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
        # Process keyword input
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
        # Reset user state
        user_states[user_id] = None

def handle_regular_message(event, msg, user_id):
    try:
        if '最新合作廠商' in msg:
            message = imagemap_message()
        elif '最新活動訊息' in msg:
            message = buttons_message()
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
        
@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
