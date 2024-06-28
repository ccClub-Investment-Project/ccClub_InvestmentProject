# from app_tools.utils import setup_project_root
# setup_project_root()

# 定義路由和視圖函數
from flask import render_template, redirect, url_for
from datetime import datetime
import logging
from app_tools.plot_creation import create_plot
from use_api.data_loader import etf_domestic_list, news, graphJSON, refresh_data # 导入预先加载的数据

def init_routes(app):
    @app.route("/keep_alive")
    def test():
        return "website Running!!!"

    @app.route('/')
    def index():
        # 放置etf info列表
        etf_domestic_count = len(etf_domestic_list)  # 计算 JSON 数据项的数量
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
        return redirect(url_for('index'))


    def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
        return datetime.fromtimestamp(value).strftime(format)

    # 添加自定义过滤器到Jinja2环境
    app.jinja_env.filters['datetimeformat'] = datetimeformat

