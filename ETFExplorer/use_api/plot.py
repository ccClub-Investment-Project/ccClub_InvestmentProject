import plotly.express as px


def create_plot(df, x_name, y_name, title="history"):
    # 生成 Plotly 圖表
    fig = px.line(df, x='Date', y='Close',
                  title='Taiwan Stock Index Over Time')
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
    # print(graphJSON)
    return graphJSON