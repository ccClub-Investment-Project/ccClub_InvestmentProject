# import os
# os.chdir('C:/python-training/ccClub_InvestmentProject/aila')
# print(os.getcwd())
import pandas as pd
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import plotly.express as px
import getdata

# 創建 Dash 應用
app = Dash(__name__)

# 從資料庫讀取數據
table = 'taiwan_stock_index_10y'
df = getdata.fetch_data_from_db(table)

# 檢查讀取的資料
print(df.head(2))
# print(df.columns)
print(df.dtypes)

# 確保日期列被識別為日期類型
if 'date' in df.columns:
    df["date"] = pd.to_datetime(df["date"])
else:
    print("Error: 'date' column not found in the DataFrame")

# 檢查讀取的資料
print(df.head(2))
# print(df.columns)
print(df.dtypes)

# 定義應用的佈局
app.layout = html.Div([
    html.H1("台股 10 年指數"),
    dcc.Dropdown(
        id='index-dropdown',
        options=[
            {'label': 'Taiwan Stock Index', 'value': 'close'}
            # 可以在這裡添加更多選項，例如 {'label': 'Another Index', 'value': 'another_column'}
        ],
        value='close',
        multi=True
    ),
    dcc.Graph(id='line-chart'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df['date'].min(),
        end_date=df['date'].max(),
        display_format='YYYY-MM-DD'
    )
])


@app.callback(
    Output('line-chart', 'figure'),
    [
        Input('index-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ]
)
def update_line_chart(selected_indices, start_date, end_date):
    print(f"Selected indices: {selected_indices}")
    print(f"Start date: {start_date}, End date: {end_date}")

    # 確保日期列被識別為日期類型
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # 過濾日期範圍內的數據
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    print(filtered_df.head())

    # 創建圖表
    fig = px.line(filtered_df, x='date', y=selected_indices,
                  title='Taiwan Stock Index Over Time')

    # 添加 rangeslider 和 rangeselector
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

    return fig


# 運行應用
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
