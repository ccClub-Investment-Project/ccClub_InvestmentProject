from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

app = Flask(__name__)

# LINE Bot API credentials
LINE_CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ImagemapSendMessage (組圖訊息)
def imagemap_message():
    message = ImagemapSendMessage(
        base_url="https://i.imgur.com/BfTFVDN.jpg",
        alt_text='最新的合作廠商有誰呢？',
        base_size=BaseSize(height=2000, width=2000),
        actions=[
            URIImagemapAction(
                link_uri="https://tw.shop.com/search/%E5%AE%B6%E6%A8%82%E7%A6%8F",
                area=ImagemapArea(x=0, y=0, width=1000, height=1000)
            ),
            URIImagemapAction(
                link_uri="https://tw.shop.com/search/%E7%94%9F%E6%B4%BB%E5%B8%82%E9%9B%86",
                area=ImagemapArea(x=1000, y=0, width=1000, height=1000)
            ),
            URIImagemapAction(
                link_uri="https://tw.shop.com/search/%E9%98%BF%E7%98%A6%E7%9A%AE%E9%9E%8B",
                area=ImagemapArea(x=0, y=1000, width=1000, height=1000)
            ),
            URIImagemapAction(
                link_uri="https://tw.shop.com/search/%E5%A1%94%E5%90%89%E7%89%B9",
                area=ImagemapArea(x=1000, y=1000, width=1000, height=500)
            ),
            URIImagemapAction(
                link_uri="https://tw.shop.com/search/%E4%BA%9E%E5%B0%BC%E5%85%8B",
                area=ImagemapArea(x=1000, y=1500, width=1000, height=500)
            )
        ]
    )
    return message

# TemplateSendMessage - ButtonsTemplate (按鈕介面訊息)
def buttons_message():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            thumbnail_image_url="https://pic2.zhimg.com/v2-de4b8114e8408d5265503c8b41f59f85_b.jpg",
            title="是否要進行抽獎活動？",
            text="輸入生日後即獲得抽獎機會",
            actions=[
                DatetimePickerTemplateAction(
                    label="請選擇生日",
                    data="input_birthday",
                    mode='date',
                    initial='1990-01-01',
                    max='2019-03-10',
                    min='1930-01-01'
                ),
                MessageTemplateAction(
                    label="看抽獎品項",
                    text="有哪些抽獎品項呢？"
                ),
                URITemplateAction(
                    label="免費註冊享回饋",
                    uri="https://tw.shop.com/nbts/create-myaccount.xhtml?returnurl=https%3A%2F%2Ftw.shop.com%2F"
                )
            ]
        )
    )
    return message

# TemplateSendMessage - CarouselTemplate (旋轉木馬模板)
def Carousel_Template():
    message = TemplateSendMessage(
        alt_text='目錄',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://example.com/image1.jpg',  # 替換為實際的圖片URL
                    title='股票功能',
                    text='請選擇以下功能',
                    actions=[
                        PostbackTemplateAction(
                            label="輸入財報",
                            data="輸入財報"
                        ),
                        PostbackTemplateAction(
                            label="基本股票功能",
                            data="基本股票功能"
                        ),
                        PostbackTemplateAction(
                            label="換股",
                            data="換股"
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://example.com/image2.jpg',  # 替換為實際的圖片URL
                    title='其他功能',
                    text='請選擇以下功能',
                    actions=[
                        PostbackTemplateAction(
                            label="個人相關功能",
                            data="個人相關功能"
                        ),
                        PostbackTemplateAction(
                            label="新聞",
                            data="新聞"
                        ),
                        URITemplateAction(
                            label="回測",
                            uri="https://tw.shop.com/nbts/create-myaccount.xhtml?returnurl=https%3A%2F%2Ftw.shop.com%2F"
                        )
                    ]
                )
            ]
        )
    )
    return message

# Function to fetch and filter news
def fetch_and_filter_news_message(keywords, limit=10):
    # Simulate fetching and filtering news based on the provided keywords
    news = [f"News related to {keyword}" for keyword in keywords][:limit]
    return "\n".join(news)

# Handling postback events
@handler.add(PostbackEvent)
def handle_postback(event):
    print(f"Handling postback event: {event.postback.data}")
    print(f"Full event data: {event}")
    if event.postback.data == "新聞":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入新聞關鍵字")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"You clicked: {event.postback.data}")
        )

# Handling message events
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(f"Message event received: {event.message.text}")
    user_input = event.message.text
    if user_input.startswith("新聞關鍵字:"):
        keywords = user_input.replace("新聞關鍵字:", "").strip().split(",")
        keywords = [k.strip() for k in keywords]  # 移除每個關鍵字前後的空格
        message = fetch_and_filter_news_message(keywords, limit=10)
        try:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="回覆消息"))
        except LineBotApiError as e:
            print(f"Error sending reply: {e}")
    else:
        # 處理其他文字消息
        line_bot_api.reply_message(
            event.reply_token,
            Carousel_Template()
        )

# LineBot server setup
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

    return 'OK'

if __name__ == "__main__":
    app.run(debug=True)
