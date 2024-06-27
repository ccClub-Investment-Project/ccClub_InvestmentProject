import requests, re
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
    parts = msg.split(',')
    input_id, amount = parts[0],parts[1]
    results = get_stock_data(input_id, int(amount))
    # 提取 id
    stock_id = results.get("id")
    # 提取 info
    stock_info = results.get("info")
    # 提取 analysis
    stock_analysis = results.get("analysis")
    # 构建字符串
    send_text = ""
    send_text += f"定期定額投資: {stock_id}\n"
    send_text += f"每月投資金額(元): {stock_info['每月投資金額(元)']}\n"
    send_text += f"累績投資金額(元): {stock_info['累績投資金額(元)']}\n"
    send_text += f"夏普值: {stock_analysis['夏普值']}\n"
    send_text += f"年化報酬率(%): {stock_analysis['年化報酬率(%)']}\n"
    send_text += f"最大回撤(%): {stock_analysis['最大回撤(%)']}\n"
    send_text += f"(Notes:不包含股利計算)"

            
    # else:
    #     send_text = "資料錯誤"
    
    message = TextMessage(text=send_text)
    # message = TextMessage(text=send_text)

    return message