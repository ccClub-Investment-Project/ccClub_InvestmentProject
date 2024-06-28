# 處理 Plotly 圖表的生成

import json
import plotly
import plotly.express as px
import yfinance as yf


def fetch_stock_data(stock_id):
    df = yf.download(stock_id)
    df.reset_index(inplace=True)
    return df


def create_plot():
    stock_id1 = '0050.TW'
    stock_id2 = '0056.TW'

    df1 = fetch_stock_data(stock_id1)
    df2 = fetch_stock_data(stock_id2)

    fig = px.line()
    fig.add_scatter(x=df1['Date'], y=df1['Close'],
                    mode='lines', name=stock_id1)
    fig.add_scatter(x=df2['Date'], y=df2['Close'],
                    mode='lines', name=stock_id2)

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
