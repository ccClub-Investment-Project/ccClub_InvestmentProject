import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# 創建 Dash 應用
app = dash.Dash(__name__)

# 讀取數據
df = pd.read_csv('taiwan_stock_index_10y.csv')

# 確保日期列被識別為日期類型
df['Date'] = pd.to_datetime(df['Date'])

# 生成標記（每年一個標記）
marks = {i: date.strftime('%Y-%m-%d') for i, date in enumerate(df['Date'][::365])}

# 定義應用的佈局
app.layout = html.Div([
    html.H1("Taiwan Stock Index 10 Years"),
    dcc.Graph(id='line-chart'),
    dcc.RangeSlider(
        id='date-range-slider',
        min=0,
        max=len(df)-1,
        value=[0, len(df)-1],
        marks=marks,
        step=1
    )
])

# 定義回調函數
@app.callback(
    Output('line-chart', 'figure'),
    [Input('date-range-slider', 'value')]
)
def update_line_chart(date_range):
    filtered_df = df.iloc[date_range[0]:date_range[1]+1]
    fig = px.line(filtered_df, x='Date', y='Close', title='Taiwan Stock Index Over Time')
    return fig

# 運行應用
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
