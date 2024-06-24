from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly
import json

app = Flask(__name__)

# 模拟数据
data = {
    'Date': pd.date_range(start='1/1/2020', periods=100).tolist(),
    'Close': pd.Series(range(100)).tolist(),
    'Volume': pd.Series(range(100, 200)).tolist()
}
df = pd.DataFrame(data)

# 渲染第一个图表的函数


def create_plot1():
    fig = px.line(df, x='Date', y='Close', title='Taiwan Stock Index Over Time',
                  line_shape='linear', render_mode='svg')
    fig.update_traces(line=dict(color='#2d2d44'), connectgaps=True)
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
        ),
        autosize=True
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# 渲染第二个图表的函数


def create_plot2():
    fig = px.bar(df, x='Date', y='Volume', title='Stock Volume Over Time')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# 根路由，展示多个图表


@app.route('/')
def index():
    graphJSON1 = create_plot1()
    graphJSON2 = create_plot2()
    return render_template('app_index_test.html', graphJSON1=graphJSON1, graphJSON2=graphJSON2)


if __name__ == '__main__':
    app.run(debug=True)
