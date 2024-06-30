import csv
from linebot.v3.messaging import TextMessage

# 讀取 CSV 文件
def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# 根據市值篩選股票
def select_by_market_cap(data, min_market_cap):
    return [row for row in data if row['市值(億)'] and float(row['市值(億)']) >= min_market_cap]

# 根據交易量篩選股票
def select_by_trading_volume(data, min_trading_volume):
    return [row for row in data if row['平均日成交額(元)'] and float(row['平均日成交額(元)']) / 100000000 >= min_trading_volume]

# 根據淨利潤篩選股票
def select_by_profit(data):
    return [row for row in data if row['2023年淨利'] and float(row['2023年淨利']) > 0]

# 根據股利發放率每年 > 0篩選股票
def select_by_constant_dividend_payout(data):
    result = []
    for row in data:
        try:
            payouts = [float(row[f'{year}年股利發放率']) for year in ['2020', '2021', '2022']]
            if all(payout > 0 for payout in payouts):
                result.append(row)
        except ValueError:
            continue
    return result

# 根據股利收益率篩選股票
def select_by_dividend_yield(data, min_yield):
    return [row for row in data if row['現金殖利率'] and float(row['現金殖利率']) >= min_yield]

# 主函數
def main(min_yield1=0):
    try:
        input_csv_file = 'stock_data_final.csv'  # Adjust the path to your CSV file
        data = read_csv(input_csv_file)
        # Part 1: select by market cap
        min_market_cap = 10
        data = select_by_market_cap(data, min_market_cap)
        # Part 2: select by trading volume
        min_trading_volume = 1
        data = select_by_trading_volume(data, min_trading_volume)
        # Part 3: select by profit > 0
        data = select_by_profit(data)
        # Part 4: select by constant dividend payout
        data = select_by_constant_dividend_payout(data)
        # Part 5: select by dividend yield
        min_yield = min_yield1 / 100  # 轉換為小數
        data = select_by_dividend_yield(data, min_yield)
        output_csv_file = 'filtered_stock_data.csv'
        fieldnames = data[0].keys()
        with open(output_csv_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        data.sort(key=lambda x: float(x['現金殖利率']), reverse=True)
        if data:
            send_text = f"共有 {len(data)} 檔股票符合條件。\n\n"
            send_text += "符合條件的股票如下：\n"
            send_text += "代號, 公司名稱, 現金殖利率\n"
            for row in data:
                send_text += f"{row['代號']}, {row['名稱']}, {float(row['現金殖利率']) * 100:.2f}%\n"
        else:
            send_text = "沒有符合條件的股票。"
        message = TextMessage(text=send_text)
        return message
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        return TextMessage(text="An error occurred while processing the data.")

if __name__ == '__main__':
    main(5)  # example argument
