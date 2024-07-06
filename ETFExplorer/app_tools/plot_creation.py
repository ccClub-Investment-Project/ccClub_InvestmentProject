# 處理 Plotly 圖表的生成

import json
import plotly
import plotly.express as px
import yfinance as yf
# from collection.api_data import api_table_data, get_strategy_yield
# from app_tools.pickle_handler import save_data, load_data
import pandas as pd
# import preload.data_loader as loader
# loader.initialize_data()

# def fetch_stock_data(stock_id):
#     df = yf.download(stock_id)
#     df.reset_index(inplace=True)
#     return df

# def create_plot1(min_yield=5):
#     strategy_yield_list = get_strategy_yield(min_yield)
    
#     fig = px.line()

#     for etf in strategy_yield_list:
#         code = int(etf['代號'])
#         stock_id = f"{code}.TW"
#         try:
#             df = fetch_stock_data(stock_id)
#         except ValueError as e:
#             stock_id = f"{code}.TWO"
#             try:
#                 df = fetch_stock_data(stock_id)
#             except ValueError as e:
#                 pass

#         fig.add_scatter(x=df['Date'], y=df['Close'],
#                     mode='lines', name=stock_id)
    
#     fig.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(count=1, label="YTD", step="year", stepmode="todate"),
#                     dict(count=1, label="1y", step="year", stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             rangeslider=dict(visible=True),
#             type="date"
#         )
#     )

#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON

# def create_plot2():
#     # etf_domestic_list = api_table_data('etf_domestic_list')
#     fig = px.line()

#     for etf in loader.etf_domestic_list:
#         code = etf['code']
#         stock_id = f"{code}.TW"
#         df = fetch_stock_data(stock_id)
#         fig.add_scatter(x=df['Date'], y=df['Close'],
#                     mode='lines', name=stock_id)
    
#     fig.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(count=1, label="YTD", step="year", stepmode="todate"),
#                     dict(count=1, label="1y", step="year", stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             rangeslider=dict(visible=True),
#             type="date"
#         )
#     )

#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON

# def create_newplot(all_plot_data, all_yield, min_yield=5):
#     # strategy_yield_list = [item for item in all_yield if item['現金殖利率'] > (min_yield/100)]
#     strategy_yield_list = get_strategy_yield(min_yield)

#     fig = px.line()

#     for etf in strategy_yield_list:
#         code = int(etf['代號'])
        
#         stock_id = f"{code}.TW"
#         if stock_id in all_plot_data:
#             df = all_plot_data[stock_id]
#         else:
#             stock_id = f"{code}.TWO"
#             df = all_plot_data[stock_id]
#         print(stock_id)
#         fig.add_scatter(x=df['Date'], y=df['Close'],
#                     mode='lines', name=stock_id)
    
#     fig.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(count=1, label="YTD", step="year", stepmode="todate"),
#                     dict(count=1, label="1y", step="year", stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             rangeslider=dict(visible=True),
#             type="date"
#         )
#     )

#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON

def plot_chart1(loader, value=5):

    # all_yield = load_data('all_yield')
    filter_yield = [item for item in loader.all_yield if item['現金殖利率'] > (value/100)]
    # codes = [pd.to_numeric(stock['代號'], errors='coerce') for stock in filter_yield]
    codes = set(int(stock['代號']) for stock in filter_yield)

    # all_history = load_data('all_history')
    # 根據 codes 生成新的字典
    filtered_dict = {key: value for key, value in loader.all_history.items() if int(key.split('.')[0]) in codes}
    # matching_keys = [key for key in all_history.keys() if key.split('.')[0] in codes]

    fig = px.line()

    # for stock_id, df in filtered_dict.items():
    #     fig.add_scatter(x=df['Date'], y=df['Close'],
    #                 mode='lines', name=stock_id)
    df_combined = pd.concat([df.assign(stock_id=key) for key, df in filtered_dict.items()])
    fig = px.line(df_combined, x='Date', y='Close', color='stock_id')


    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_chart2(loader):
    # etf_domestic_list = api_table_data('etf_domestic_list')
    fig = px.line()

    for stock_id, df in loader.all_etf_history.items():
        fig.add_scatter(x=df['Date'], y=df['Close'],
                    mode='lines', name=stock_id)
    
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
