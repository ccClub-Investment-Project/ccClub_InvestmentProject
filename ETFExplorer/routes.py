# from app_tools.utils import setup_project_root
# setup_project_root()

# 定義路由和視圖函數
from flask import render_template, redirect, url_for, request, jsonify, Blueprint, make_response
from datetime import datetime
import logging, time
from app_tools.plot_creation import plot_chart1, plot_chart2
# 預先把資料讀進來
from preload.data_loader import all_yield,etf_domestic_list, etf_performance,all_history, all_etf_history
# loader.initialize_data()

# from preload.data_loader import etf_domestic_list, etf_performance, graphJSON1, graphJSON2 # 导入预先加载的数据
from collection.api_data import get_news_data, get_strategy_yield


# 創建一個藍圖（Blueprint）
main = Blueprint('main', __name__)


def configure_routes(app, cache):

    @app.route("/keep_alive")
    def test():
        return "website Running!!!"
    
    @cache.memoize(timeout=300)
    def get_news():
        return get_news_data('台股,美股', True, 25)

    @app.route('/update_yield')
    def update_yield():
        value = request.args.get('value', type=int)
        filtered_df = all_yield.loc[all_yield['現金殖利率'] > (value / 100)]
        filtered_df = filtered_df[['代號', '名稱', '現金殖利率']]
        updated_data = filtered_df.to_dict(orient='records')
        # 將更新後的數據轉換為 JSON 格式
        return jsonify(updated_data)


    @app.route('/update_plot')
    def update_plot():
        value = request.args.get('value', type=int)

        # 檢查是否已有快取的結果
        cache_key = f"update_plot_{value}"
        cached_result = cache.get(cache_key)        
        if cached_result:
            return cached_result

        # 沒有快取結果，生成圖表
        graphJSON1 = plot_chart1(value)
        if not graphJSON1:
            return jsonify({"error": "Failed to generate plot"}), 503

        # 將結果包裝成 Flask 回應
        response = make_response(graphJSON1)
        response.headers['Content-Type'] = 'application/json'

        # 快取成功的結果
        cache.set(cache_key, response, timeout=86400)
        return response
    
        # graphJSON1 = plot_chart1(value)
        # return graphJSON1

    @app.route('/')
    def index():
        # 讀取資料
        news = get_news()
        # 計算ETF數量
        etf_domestic_count = len(etf_domestic_list)
        # 計算策略篩選出來數量
        strategy_yield_count = len(get_strategy_yield(5))

        return render_template('app.html',
            graphJSON1= plot_chart1(5),
            graphJSON2= plot_chart2(),
            etf_domestic_list = etf_domestic_list,
            etf_performance = etf_performance,
            etf_domestic_count = etf_domestic_count,
            strategy_yield_count = strategy_yield_count,
            news_list=news, 
            strategy_yield = get_strategy_yield,
            )

    @app.route('/refresh_data')
    def refresh():
        logging.info("Refreshing data")
        # refresh_data()
        # cache.clear()  # 清除所有緩存
        return redirect(url_for('index'))


    def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
        return datetime.fromtimestamp(value).strftime(format)

    # 添加自定义过滤器到Jinja2环境
    app.jinja_env.filters['datetimeformat'] = datetimeformat

    app.register_blueprint(main)