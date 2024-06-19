from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import os
from dotenv import load_dotenv
load_dotenv()
from linebot.models import TemplateSendMessage, CarouselTemplate, CarouselColumn, MessageAction, URIAction


app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

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
from linebot.models import *

def buttons_message1():
    message = TemplateSendMessage(
        alt_text='Buttons template 1',
        template=ButtonsTemplate(
            actions=[
                MessageTemplateAction(
                    label="查詢股票資訊",
                    text="查詢股票資訊"
                ),
                MessageTemplateAction(
                    label="歷史股價查詢",
                    text="歷史股價查詢"
                )
            ]
        )
    )
    return message

def buttons_message2():
    message = TemplateSendMessage(
        alt_text='Buttons template 2',
        template=ButtonsTemplate(
            actions=[
                MessageTemplateAction(
                    label="換股時間",
                    text="換股時間"
                ),
                MessageTemplateAction(
                    label="換了哪些股",
                    text="換了哪些股"
                )
            ]
        )
    )
    return message

def Carousel_Template():
    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://example.com/item1.jpg',
                    title='股票相關功能',
                    text='Description 1',
                    actions=[
                        MessageAction(
                            label='財報',
                            text='財報'
                        ),
                        MessageAction(
                            label='基本股票功能',
                            text='基本股票功能'
                        ),
                        MessageAction(
                            label='換股',
                            text='換股'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://example.com/item2.jpg',
                    title='其他相關功能',
                    text='Description 2',
                    actions=[
                        MessageAction(
                            label='個人相關功能',
                            text='個人相關功能'
                        ),
                        MessageAction(
                            label='新聞',
                            text='新聞'
                        ),
                        MessageAction(
                            label='回測',
                            text='新聞'
                        )
                    ]
                )
            ]
        )
    )
    return carousel_template_message




# Webhook route
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
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run()
