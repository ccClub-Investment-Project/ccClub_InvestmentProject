import requests
class CnyesNewsSpider:
    def get_latest_news(self, pages=10, limit=10):
        headers = {
            'Origin': 'https://news.cnyes.com/',
            'Referer': 'https://news.cnyes.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        all_news = []
        for page in range(1, pages + 1):
            try:
                r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/headline?page={page}&limit={limit}", headers=headers, timeout=10)
                r.raise_for_status()  # 如果響應不是200，這將拋出異常
                data = r.json()
                print(f"API Response Page {page}: {data}")  # 打印每個頁面的響應
                all_news.extend(data.get('items', {}).get('data', []))
            except requests.RequestException as e:
                print(f"請求第{page}頁新聞失敗: {e}")
                break
            except ValueError as e:
                print(f"解析第{page}頁 JSON 失敗: {e}")
                break
        return all_news

    def filter_news(self, newslist, keywords):
        filtered_news = []
        for news in newslist:
            if any(keyword.lower() in news.get("title", "").lower() for keyword in keywords):
                filtered_news.append(news)
        return filtered_news
