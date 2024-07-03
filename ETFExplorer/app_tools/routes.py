# from app_tools.utils import setup_project_root
# setup_project_root()

# 定義路由和視圖函數
from flask import render_template, redirect, url_for, request, jsonify
from datetime import datetime
import logging, time
from app_tools.plot_creation import create_plot1
# 預先把資料讀進來
from use_api.data_loader import etf_domestic_list, etf_performance, graphJSON1, graphJSON2 # 导入预先加载的数据
from use_api.data_loader import refresh_data
from use_api.data import get_news_data, api_table_data, get_strategy_basic, get_strategy_yield

def init_routes(app, cache):

    @app.route("/keep_alive")
    def test():
        return "website Running!!!"
    
    @cache.memoize(timeout=300)
    def get_news():
        return get_news_data('台股,美股', True, 25)

    @app.route('/update_yield')
    def update_yield():
        value = request.args.get('value', type=int)
        # 調用 get_strategy_yield 函數，傳入選擇的值
        updated_data = get_strategy_yield(value)
        # 將更新後的數據轉換為 JSON 格式
        return jsonify(updated_data)

    @app.route('/update_plot')
    def update_plot():
        value = request.args.get('value', type=int)
        # 調用 create_plot1 函數，傳入選擇的值
        graphJSON1 = create_plot1(value)
        return graphJSON1

    @app.route('/')
    def index():
        # 讀取資料
        news = get_news()
        # 計算ETF數量
        etf_domestic_count = len(etf_domestic_list)
        #
        strategy_yield_count = len(get_strategy_yield(5))
        # test - 定义变量
        # items = ['Apple', 'Banana', 'Cherry']
        # extra_info = 'This is some extra information.'


        return render_template('app.html',
            graphJSON1=graphJSON1,
            graphJSON2=graphJSON2,
            etf_domestic_list = etf_domestic_list,
            etf_performance = etf_performance,
            etf_domestic_count = etf_domestic_count,
            strategy_yield_count = strategy_yield_count,
            news_list=news, 
            # strategy_basic = get_strategy_basic,
            strategy_yield = get_strategy_yield,
            # items=items, 
            # extra_info=extra_info
            )

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

