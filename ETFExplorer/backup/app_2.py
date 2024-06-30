import os  # noqa: E402
import sys  # noqa: E402
from datetime import datetime
print(os.getcwd())  # noqa: E402
# 确保当前工作目录为项目的根目录
current_path = os.path.dirname(os.path.abspath(__file__))  # noqa: E402
project_root = os.path.join(current_path, '..')  # noqa: E402
sys.path.insert(0, project_root)  # noqa: E402
os.chdir(project_root)  # noqa: E402

# cd ccClub_InvestmentProject/aila
import json
import plotly
import plotly.express as px
import pandas as pd
from flask import Flask, render_template
from use_pg_SQL.getdata import fetch_data_from_db
from use_api.data import get_news_data

app = Flask(__name__)

# 從資料庫讀取數據
# table = 'taiwan_stock_index_10y'
# df = fetch_data_from_db(table)

# 確保日期列被識別為日期類型
# df["Date"] = pd.to_datetime(df["Date"])

# 測試讀取yahoo finance
import yfinance as yf
stock_id1 = '0050.TW'
df1 = yf.download(stock_id1)
# 将索引重置为列
df1.reset_index(inplace=True)

stock_id2 = '0056.TW'
df2 = yf.download(stock_id2)
# 将索引重置为列
df2.reset_index(inplace=True)


def create_plot():
    # 生成 Plotly 圖表
    fig = px.line()
    fig.add_scatter(x=df1['Date'], y=df1['Close'], mode='lines', name=stock_id1)
    fig.add_scatter(x=df2['Date'], y=df2['Close'], mode='lines', name=stock_id2)
    # fig = px.line(df, x='Date', y='Close',
    #               title='0050')

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

# 渲染第一个图表的函数
# def create_plot1():
#     fig = px.line(df, x='Date', y='Close', title='Taiwan Stock Index Over Time',
#                   line_shape='linear', render_mode='svg')
#     fig.update_traces(line=dict(color='#2d2d44'), connectgaps=True)
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
#         ),
#         autosize=True
#     )
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON
# # 渲染第二个图表的函数


# def create_plot2():
#     fig = px.bar(df, x='Date', y='Volume', title='Stock Volume Over Time')
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON
@app.route("/keep_alive")
def test():
    return "website Running!!!"


@app.route('/')
def index():
    graphJSON = create_plot()
    
    # 放置策略1的圖表 (放置許多ETF) 讀取 yahoo finance
    
    # 放置新聞區塊
    news = get_news_data('台股,美股', True, 25)  # 获取新闻数据

    # graphJSON1 = create_plot1()
    # graphJSON2 = create_plot2()
    # print(graphJSON)
    # return render_template('app_0619_merge.html', graphJSON=graphJSON, graphJSON1=graphJSON1, graphJSON2=graphJSON2)
    return render_template('app_0619_merge.html', graphJSON=graphJSON,  news_list=news)

    

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.fromtimestamp(value).strftime(format)

# 添加自定义过滤器到Jinja2环境
app.jinja_env.filters['datetimeformat'] = datetimeformat

if __name__ == '__main__':
    app.run(debug=True)