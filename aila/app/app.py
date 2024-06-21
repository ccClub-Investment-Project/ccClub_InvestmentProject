# import os  # noqa: E402
# os.chdir('C:/python-training/ccClub_InvestmentProject')  # noqa: E402
# print(os.getcwd())  # noqa: E402

import os
import sys

# 获取上一级目录路径
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa: E402
# 将上一级目录添加到 sys.path
sys.path.insert(0, parent_dir)  # noqa: E402

# 打印调试信息，确保路径正确
print(f"Parent directory: {parent_dir}")  # noqa: E402
print(f"Files in parent directory: {os.listdir(parent_dir)}")  # noqa: E402


from use_pg_SQL.getdata import fetch_data_from_db

# import parent_module
from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly
# from use_pg_SQL import getdata
import json


# 获取上一级目录路径
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将上一级目录添加到 sys.path
sys.path.insert(0, parent_dir)

# 打印调试信息，确保路径正确
print(f"Parent directory: {parent_dir}")
print(f"Files in parent directory: {os.listdir(parent_dir)}")


app = Flask(__name__)

# 從資料庫讀取數據
table = 'taiwan_stock_index_10y'
df = fetch_data_from_db(table)

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

    return render_template('app_0619_merge.html', graphJSON=graphJSON)


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000, threads=4)
