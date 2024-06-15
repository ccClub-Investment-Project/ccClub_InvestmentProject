import os
from aila.use_pg_SQL import getdata
import json
import plotly
import plotly.express as px
import pandas as pd
from flask import Flask, render_template
import parent_module
import sys


# 获取父目录路径
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


parent_module.parent_function()

# os.chdir('C:/python-training/ccClub_InvestmentProject/aila/app')
print(os.getcwd())


app = Flask(__name__)

# 從資料庫讀取數據
table = 'taiwan_stock_index_10y'
df = getdata.fetch_data_from_db(table)

# 確保日期列被識別為日期類型
df["Date"] = pd.to_datetime(df["Date"])


@app.route('/')
def index():
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

    return render_template('app_index.html', graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(debug=True)
