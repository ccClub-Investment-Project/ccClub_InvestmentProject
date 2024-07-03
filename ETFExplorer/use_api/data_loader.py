from use_api.data import get_news_data, api_table_data
from app_tools.plot_creation import create_plot1, create_plot2
# 在模块加载时获取数据并存储在变量中
etf_domestic_list = api_table_data('etf_domestic_list')
news = get_news_data('台股,美股', True, 25)
# tab1的圖
graphJSON1 = create_plot1(5)
# tab2的圖
graphJSON2 = create_plot2()

def refresh_data():
    global etf_domestic_list, news, graphJSON
    etf_domestic_list = api_table_data('etf_domestic_list')
    news = get_news_data('台股,美股', True, 25)
    graphJSON1 = create_plot1(5)
    graphJSON2 = create_plot2()