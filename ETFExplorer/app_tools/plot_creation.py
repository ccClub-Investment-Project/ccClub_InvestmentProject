# 處理 Plotly 圖表的生成

import json
import plotly
import plotly.express as px
import yfinance as yf
from use_api.data import api_table_data, get_strategy_yield


def fetch_stock_data(stock_id):
    df = yf.download(stock_id)
    df.reset_index(inplace=True)
    return df

def create_plot1(min_yield=5):
    strategy_yield_list = get_strategy_yield(min_yield)
    
    fig = px.line()

    for etf in strategy_yield_list:
        code = int(etf['代號'])
        stock_id = f"{code}.TW"
        try:
            df = fetch_stock_data(stock_id)
        except ValueError as e:
            stock_id = f"{code}.TWO"
            try:
                df = fetch_stock_data(stock_id)
            except ValueError as e:
                pass

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

def create_plot2():
    etf_domestic_list = api_table_data('etf_domestic_list')
    fig = px.line()

    for etf in etf_domestic_list:
        code = etf['code']
        stock_id = f"{code}.TW"
        df = fetch_stock_data(stock_id)
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


def create_newplot(all_plot_data, all_yield, min_yield=5):
    # strategy_yield_list = [item for item in all_yield if item['現金殖利率'] > (min_yield/100)]
    strategy_yield_list = get_strategy_yield(min_yield)

    fig = px.line()

    for etf in strategy_yield_list:
        code = int(etf['代號'])
        
        stock_id = f"{code}.TW"
        if stock_id in all_plot_data:
            df = all_plot_data[stock_id]
        else:
            stock_id = f"{code}.TWO"
            df = all_plot_data[stock_id]
        print(stock_id)
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

