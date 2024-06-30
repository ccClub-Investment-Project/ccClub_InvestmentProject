import requests, re, math
from linebot.v3.messaging import TextMessage

def get_stock_data(id, amount=6000):
    url = 'https://backtest-kk2m.onrender.com/backtest/{id}'.format(id=id)
    params = {
        'amount': amount,
    }
    response = requests.get(url, params=params)
    return response.json()

# for 定期定額使用
def backtest(msg):
    try:
        send_text = ""
        parts = msg.split(',')
        if len(parts) == 2:
            input_id, amount = parts[0],parts[1]
            results = get_stock_data(input_id, int(amount))

        elif len(parts) ==1:
            input_id = parts[0]
            results = get_stock_data(input_id)
        else:
            results = get_stock_data("0050")  
        # 提取 id
        stock_id = results.get("id")
        # 提取 info
        stock_info = results.get("info")
        # 提取 analysis
        stock_analysis = results.get("analysis")
        # 提取 log
        stock_log = results.get("log")
        # 构建字符串
        money = stock_info['每月投資金額(元)']
        send_text += f"每個月定期定額: {money}元\n"
        send_text += f"投資標的: {stock_id}\n"
        send_text += f"回測範圍: {stock_info['回測範圍(年)']}年\n"
        send_text += f"累績投資金額: {stock_info['累績投資金額(元)']}元\n"
        send_text += f"夏普值: {stock_analysis['夏普值']}\n"
        send_text += f"年化報酬率: {stock_analysis['年化報酬率(%)']}%\n"
        send_text += f"最大回撤: {stock_analysis['最大回撤(%)']}%\n"
        send_text += f"(Notes:不包含股利計算)"
    except Exception as error:
        send_text = "資料錯誤"
        print("An error occurred:", error)
        
    message = TextMessage(text=send_text)

    return message