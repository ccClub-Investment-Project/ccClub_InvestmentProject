from use_api.data import get_news_data, api_table_data, get_strategy_yield, get_all_plot_data
from app_tools.plot_creation import create_plot1, create_plot2
from app_tools.preload_data import save_data, load_data

# 在模块加载时获取数据并存储在变量中
etf_domestic_list = load_data('etf_domestic_list')
etf_performance = load_data('etf_performance')
# all_yield = get_strategy_yield(0)
# all_plot_data = get_all_plot_data()
news = get_news_data('台股,美股', True, 25)
# tab1的圖
graphJSON1 = create_plot1(5)
# tab2的圖
graphJSON2 = create_plot2()


def refresh_data():
    # 從api 更新數據
    etf_domestic_list = api_table_data('etf_domestic_list')
    save_data(etf_domestic_list,'etf_domestic_list')
    # 從api 更新數據
    etf_performance = api_table_data('etf_performance')
    save_data(etf_performance,'etf_performance')



    pass
    # global etf_domestic_list, news, graphJSON
    # etf_domestic_list = api_table_data('etf_domestic_list')
    # etf_performance = api_table_data('etf_performance')
    # news = get_news_data('台股,美股', True, 25)
    # graphJSON1 = create_plot1(5)
    # graphJSON2 = create_plot2()
    # all_yield = get_strategy_yield(0)
    # all_plot_data = get_all_plot_data()
