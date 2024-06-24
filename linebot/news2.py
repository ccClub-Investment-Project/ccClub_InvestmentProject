from linebot.v3.messaging import TextMessage
from news import CnyesNewsSpider

def fetch_and_filter_news_message(keywords, pages=10, limit=10):
    cnyes_news_spider = CnyesNewsSpider()
    latest_news = cnyes_news_spider.get_latest_news(pages=pages, limit=limit)
    print(f"Latest News: {latest_news}")  # 檢查最新新聞

    if latest_news:
        filtered_news = cnyes_news_spider.filter_news(latest_news, keywords)
        # 構建新聞列表消息
        news_list_text = "最新新聞:\n\n"
        for index, news in enumerate(filtered_news, 1):
            news_list_text += f"{index}. {news['title']}\n"
            news_list_text += f"   連結: https://news.cnyes.com/news/id/{news['newsId']}\n\n"

        if filtered_news:
            message = TextMessage(text=news_list_text.strip())
        else:
            message = TextMessage(text="最新新聞中沒有找到相關內容。")
    else:
        message = TextMessage(text="無法獲取最新新聞，請稍後再試。")
    
    return message
