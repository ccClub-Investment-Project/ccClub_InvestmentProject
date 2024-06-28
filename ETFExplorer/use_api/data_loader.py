from use_api.data import get_news_data, api_table_data
from app_tools.plot_creation import create_plot
# 在模块加载时获取数据并存储在变量中
etf_domestic_list = api_table_data('etf_domestic_list')
news = get_news_data('台股,美股', True, 25)
graphJSON = create_plot()

def refresh_data():
    global etf_domestic_list, news, graphJSON
    etf_domestic_list = api_table_data('etf_domestic_list')
    news = get_news_data('台股,美股', True, 25)
    graphJSON = create_plot()