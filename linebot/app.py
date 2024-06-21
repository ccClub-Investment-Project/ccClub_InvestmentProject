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

# Custom module imports
from message import *
from news import *
from Function import *

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load environment variables
channel_access_token = os.getenv('channel_access_token')
channel_secret = os.getenv('channel_secret')
port = int(os.getenv('PORT', 5000))

# Debugging: Print the channel access token and channel secret
print(f"Channel Access Token: {channel_access_token}")
print(f"Channel Secret: {channel_secret}")

if not channel_access_token:
    raise ValueError("The channel access token is not set. Please check your environment variables.")
if not channel_secret:
    raise ValueError("The channel secret is not set. Please check your environment variables.")

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
    line_bot_api = MessagingApi(ApiClient(configuration))  # Use MessagingApi directly with ApiClient
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
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[error_message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = None

def handle_keywords_input(line_bot_api, event, msg, user_id):
    try:
        keywords = [keyword.strip() for keyword in msg.split(',') if keyword.strip()]
        if keywords:
            logging.info(f"Fetching news for keywords: {keywords}")
            message = fetch_and_filter_news_message(keywords, limit=10)

            # Check if message is a TextMessage object
            if isinstance(message, TextMessage):
                logging.info(f"Fetched news: {message.text[:100]}...")  # Log first 100 chars of the text
                reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
            else:
                # If not a TextMessage object, convert to string
                message_str = str(message)
                logging.info(f"Fetched news: {message_str[:100]}...")  # Log first 100 chars
                reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=message_str)])

            line_bot_api.reply_message(reply_message)
        else:
            prompt_message = TextMessage(text="請輸入有效的關鍵字，用逗號分隔:")
            reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[prompt_message])
            line_bot_api.reply_message(reply_message)
    except Exception as e:
        logging.error(f"Error in handle_keywords_input: {e}", exc_info=True)
        error_message = TextMessage(text="獲取新聞時發生錯誤，請稍後再試。")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[error_message])
        line_bot_api.reply_message(reply_message)
    finally:
        user_states[user_id] = None

def handle_regular_message(line_bot_api, event, msg, user_id):
    if '財報' in msg:
        message = buttons_message1()
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
    elif '基本股票功能' in msg:
        message = buttons_message1()
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        return
    elif '換股' in msg:
        message = buttons_message2()
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        return
    elif '目錄' in msg:
        carousel = Carousel_Template()
        logging.info(f"Carousel_Template 返回的消息: {carousel}")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[carousel])
        line_bot_api.reply_message(reply_message)
        return
    elif '新聞' in msg:
        message = TextMessage(text="請輸入關鍵字，用半形逗號分隔:")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = 'waiting_for_keywords'
        return
    elif '功能列表' in msg:
        message = function_list()
    elif '回測' in msg:
        message = TextMessage(text="請問要回測哪一支,定期定額多少,幾年(請用半形逗號隔開):")
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)
        user_states[user_id] = 'waiting_for_backtest'
        return

    if user_states.get(user_id) == 'waiting_for_backtest':
        try:
            logging.info(f"收到回測輸入: {msg}")
            result = backtest(msg)
            logging.info(f"回測結果: {result}")

            def format_backtest_result(result):
                result_str = str(result)
                start = result_str.find("text='") + 6
                end = result_str.rfind("'")
                content = result_str[start:end]
                formatted_result = content.replace("\\n", "\n")
                return formatted_result

            formatted_result = format_backtest_result(result)
            message = TextMessage(text=formatted_result)
            reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
            line_bot_api.reply_message(reply_message)

        except ValueError as e:
            logging.error(f"解析輸入時發生錯誤: {e}")
            message = TextMessage(text="輸入格式錯誤，請按照 '標的,定期定額,年數' 的格式輸入")
            reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
            line_bot_api.reply_message(reply_message)
        except Exception as e:
            logging.error(f"回測過程中發生錯誤: {e}")
            message = TextMessage(text="回測過程中發生錯誤，請稍後再試")
            reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
            line_bot_api.reply_message(reply_message)
        finally:
            user_states[user_id] = None
        return


@handler.add(MemberJoinedEvent)
def welcome(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        uid = event.joined.members[0].user_id
        gid = event.source.group_id
        profile = line_bot_api.get_group_member_profile(gid, uid)
        name = profile.display_name
        message = TextMessage(text=f'{name}歡迎加入')
        reply_message = ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
        line_bot_api.reply_message(reply_message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
