# 處理 Plotly 圖表的生成

import json
import plotly
import plotly.express as px
import yfinance as yf
from use_api.data import api_table_data


def fetch_stock_data(stock_id):
    df = yf.download(stock_id)
    df.reset_index(inplace=True)
    return df


def create_plot():
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
