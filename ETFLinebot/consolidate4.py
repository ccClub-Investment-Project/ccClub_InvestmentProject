# for linebot strategy!!!!
from consolidate3 import strategy_basic, strategy_yield
from linebot.v3.messaging import TextMessage

# Get the top n stocks ordered by yield
def main_n(top_n=20):
    top_n = int(top_n)  # Convert top_n to an integer
    df = strategy_basic(n=top_n).df_filtered
    if top_n > len(df):
        top_n = len(df)
    title = f"以下是殖利率由高到低排序的前 {top_n} 檔股票：\n\n"
    message = show(df, title)
    return message

# filter by yield
def main(min_yield=0):
    df = strategy_yield(min_yield).df_filtered
    title = f"共有 {len(df)} 檔股票符合條件。\n\n"
    title += "符合條件的股票如下：\n"
    message = show(df, title)
    return message    

def show(df, title):
    if not df.empty:
        send_text = title
        send_text += "代號, 公司名稱, 現金殖利率\n"
        for _, row in df.iterrows():
            send_text += f"{row['代號']}, {row['名稱']}, {row['現金殖利率'] * 100:.2f}%\n"
    else:
        send_text = "沒有符合條件的股票。"
    print(send_text)  
    message = TextMessage(text=send_text)
    return message

# main_n(20)
# main(6)        
        
# if __name__ == '__main__':
#     main(10)  # example argument