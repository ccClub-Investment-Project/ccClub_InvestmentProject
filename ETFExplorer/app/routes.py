# 定義路由和視圖函數

from flask import render_template
from app.plot_creation import create_plot
from use_api.data import get_news_data
from datetime import datetime

def init_routes(app):
    @app.route("/keep_alive")
    def test():
        return "website Running!!!"

    @app.route('/')
    def index():
        graphJSON = create_plot()

        # 放置新聞區塊
        news = get_news_data('台股,美股', True, 25)  # 获取新闻数据

        return render_template('app.html', graphJSON=graphJSON, news_list=news)

    def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
        return datetime.fromtimestamp(value).strftime(format)

    # 添加自定义过滤器到Jinja2环境
    app.jinja_env.filters['datetimeformat'] = datetimeformat