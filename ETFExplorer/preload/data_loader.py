from collection.api_data import get_news_data, api_table_data, get_strategy_yield, get_all_plot_data
# ------- 以下未整理 ------

# from app_tools.plot_creation import create_plot2
from app_tools.pickle_handler import save_data, load_data

etf_domestic_list = None
etf_performance = None
twse_listed = None
tpex_listed = None
all_yield = None
all_history = None
# 以下還沒處理
news, graphJSON1, graphJSON2 = None, None, None

def initialize_data():
    global etf_domestic_list, etf_performance
    etf_domestic_list = load_data('etf_domestic_list')
    etf_performance = load_data('etf_performance')
    global twse_listed, tpex_listed
    twse_listed = load_data('twse_listed')
    tpex_listed = load_data('tpex_listed')
    global all_yield, all_history, all_etf_history
    all_yield = load_data('all_yield')
    all_history = load_data('all_history')
    all_etf_history = load_data('all_etf_history')
    # 即時更新
    global news
    news = get_news_data('台股,美股', True, 25)
    # 以下還沒處理
    # global graphJSON1, graphJSON2
    # tab1的圖
    # graphJSON1 = plot_chart(4)
    # tab2的圖
    # graphJSON2 = create_plot2()

# if __name__ == "__main__":
#     print("Loading preload file")
#     initialize_data()
