from dotenv import load_dotenv
load_dotenv()

# 測試linebot
from flask import Flask, request, abort
import os
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.webhook import WebhookHandler

# 設置您的 Channel Access Token 和 Channel Secret
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('CHANNEL_SECRET')

# print(channel_access_token,channel_secret)

app = Flask(__name__)

configuration = Configuration(access_token=channel_access_token)
line_bot_api = MessagingApi(configuration)
handler = WebhookHandler(channel_secret)

@app.route('/')
def index():
    return "Hello World"

@app.route('/test')
def test():
    return "Test Route"

# 執行內容
if __name__ == "__main__":
    port = int(os.getenv('line_port', 5555))
    app.run(host='0.0.0.0', port=port)