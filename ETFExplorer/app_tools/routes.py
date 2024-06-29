# from app_tools.utils import setup_project_root
# setup_project_root()

# 定義路由和視圖函數
from flask import render_template, redirect, url_for

from datetime import datetime
import logging, time
from app_tools.plot_creation import create_plot
# 預先把資料讀進來
from use_api.data_loader import etf_domestic_list, graphJSON, refresh_data # 导入预先加载的数据
from use_api.data_loader import graphJSON, refresh_data # 导入预先加载的数据

from use_api.data import get_news_data, api_table_data

def init_routes(app, cache):

    @app.route("/keep_alive")
    def test():
        return "website Running!!!"
    
    @cache.memoize(timeout=86400)
    def get_news():
        return get_news_data('台股,美股', True, 25)


    @app.route('/')
    def index():
        # 讀取資料
        news = get_news()
        # 計算ETF數量
        etf_domestic_count = len(etf_domestic_list)
        # 定义变量
        items = ['Apple', 'Banana', 'Cherry']
        extra_info = 'This is some extra information.'

        return render_template('app.html', 
            graphJSON=graphJSON,
            etf_domestic_list = etf_domestic_list,
            etf_domestic_count = etf_domestic_count,
            news_list=news, 
            items=items, 
            extra_info=extra_info)

    @app.route('/refresh_data')
    def refresh():
        logging.info("Refreshing data")
        refresh_data()
        # cache.clear()  # 清除所有緩存
        return redirect(url_for('index'))


    def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
        return datetime.fromtimestamp(value).strftime(format)

    # 添加自定义过滤器到Jinja2环境
    app.jinja_env.filters['datetimeformat'] = datetimeformat

