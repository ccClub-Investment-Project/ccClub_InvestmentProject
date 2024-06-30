



# Part 1: select by market cap
# Part 2: select by trading volume
# Part 3: select by profit > 0
# Part 4: select by constant dividend payout
# Part 4: select by dividend yield


import csv


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


# 連結line bot的選股函數


# 對於股市小白提供前十名的殖利率
# def filter_top_10_dividend_stocks():
#     input_csv_file = 'web_scraping_raw_data/stock_data_final.csv'
#     data = read_csv(input_csv_file)
#
#     # 過濾掉無效的現金殖利率值
#     filtered_data = []
#     for row in data:
#         try:
#             if row['現金殖利率'] and float(row['現金殖利率']) >= 0:
#                 filtered_data.append(row)
#         except ValueError:
#             continue
#
#     # 按現金殖利率排序，排除空值
#     filtered_data.sort(key=lambda x: float(x['現金殖利率']), reverse=True)
#
#     top_10_stocks = filtered_data[:10]  # 取前10檔股票
#
#     # 只保留需要的欄位
#     top_10_stocks = [{'代號': row['代號'], '名稱': row['名稱'], '現金殖利率': row['現金殖利率']} for row in top_10_stocks]
#
#     output_csv_file = 'web_scraping_raw_data/top_10_dividend_stocks.csv'
#     fieldnames = ['代號', '名稱', '現金殖利率']
#
#     with open(output_csv_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
#         writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(top_10_stocks)
#
#     print(f"前十名的殖利率最高的股票已保存到 {output_csv_file}")
#     print("\n前十名的殖利率最高的股票如下：")
#     print("代號, 公司名稱, 現金殖利率")
#     for row in top_10_stocks:
#         print(f"{row['代號']}, {row['名稱']}, {float(row['現金殖利率']) * 100: .2f}%")
# 在 Samantha.py 中增加以下功能：
def filter_top_10_dividend_stocks():
    try:
        # 讀取 CSV 文件
        file_path = "web_scraping_raw_data/stock_data_final.csv"
        data = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        # 按現金殖利率排序，選出前 10 名
        data.sort(key=lambda x: float(x['現金殖利率']) if x['現金殖利率'] else 0, reverse=True)
        top_10_stocks = data[:10]

        # 回傳前 10 名的股票**
        return top_10_stocks
    except Exception as e:
        logging.error(f"Error in filtering top 10 dividend stocks: {e}")
        return []


def filter_stocks(market_cap, trading_volume, profit_or_not, payout, dividend_yield):
    input_csv_file = 'web_scraping_raw_data/stock_data_final.csv'
    data = read_csv(input_csv_file)

    # Part 1: select by market cap
    data = select_by_market_cap(data, market_cap)

    # Part 2: select by trading volume
    data = select_by_trading_volume(data, trading_volume)

    # Part 3: select by profit > 0
    if profit_or_not == 'Y':
        data = select_by_profit(data)

    # Part 4: select by constant dividend payout
    if payout == 'Y':
        data = select_by_constant_dividend_payout(data)

    # Part 5: select by dividend yield
    data = select_by_dividend_yield(data, dividend_yield)

    if data:
        # 按照現金殖利率排序
        data.sort(key=lambda x: float(x['現金殖利率']), reverse=True)
        # 返回結果
        return data
    else:
        return []

# 主函數

# 主函數
def main():
    print("您是股市小白還是股市高手？")
    print("1. 股市小白")
    print("2. 股市高手")

    choice = input("請選擇 (1/2): ").strip()

    if choice == '1':
        filter_top_10_dividend_stocks()
    elif choice == '2':
        print("請輸入篩選條件：")

        # 讀取 CSV 文件
        input_csv_file = 'web_scraping_raw_data/stock_data_final.csv'
        data = read_csv(input_csv_file)

        # Part 1: select by market cap
        min_market_cap = float(input("請輸入最小市值 (億): "))
        data = select_by_market_cap(data, min_market_cap)

        # Part 2: select by trading volume
        min_trading_volume = float(input("請輸入最小日交易量 (億): "))
        data = select_by_trading_volume(data, min_trading_volume)

        # Part 3: select by profit > 0
        while True:
            profit_or_not = input("前一年是否獲利(Y/N): ").strip().upper()
            if profit_or_not == 'Y':
                data = select_by_profit(data)
                break
            elif profit_or_not == 'N':
                break
            else:
                print("請輸入 'Y' 或 'N'")

        # Part 4: select by constant dividend payout
        while True:
            payout = input("是否連續三年發放現金股利(Y/N): ").strip().upper()
            if payout == "Y":
                data = select_by_constant_dividend_payout(data)
                break
            elif payout == "N":
                break
            else:
                print("請輸入 'Y' 或 'N'")

        # Part 5: select by dividend yield
        min_yield = float(input("請輸入最小現金殖利率 (%): ")) / 100  # 轉換為小數
        data = select_by_dividend_yield(data, min_yield)

        output_csv_file = 'web_scraping_raw_data/filtered_stock_data.csv'
        fieldnames = data[0].keys()

        with open(output_csv_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        # 按照現金殖利率排序
        data.sort(key=lambda x: float(x['現金殖利率']), reverse=True)

        if data:
            fieldnames = data[0].keys()
            with open(output_csv_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            print(f"篩選後的股票數據已保存到 {output_csv_file}")
            print(f"共有 {len(data)} 檔股票符合條件。")

            print("\n符合條件的股票如下：")
            print("代號, 公司名稱, 現金殖利率")
            for row in data:
                print(f"{row['代號']}, {row['名稱']}, {float(row['現金殖利率']) * 100: .2f}%")
        else:
            print("沒有符合條件的股票。")
    else:
        print("請選擇 '1' 或 '2'")

# def main():
#     input_csv_file = 'web_scraping_raw_data/stock_data_final.csv'
#     data = read_csv(input_csv_file)
#
#     print("請輸入篩選條件：")
#
#     # Part 1: select by market cap
#     min_market_cap = float(input("請輸入最小市值 (億): "))
#     data = select_by_market_cap(data, min_market_cap)
#
#     # Part 2: select by trading volume
#     min_trading_volume = float(input("請輸入最小日交易量 (億): "))
#     data = select_by_trading_volume(data, min_trading_volume)
#
#     # Part 3: select by profit > 0
#     while True:
#         profit_or_not = input("前一年是否獲利(Y/N): ").strip().upper()
#         if profit_or_not == 'Y':
#             data = select_by_profit(data)
#             break
#         elif profit_or_not == 'N':
#             break
#         else:
#             print("請輸入 'Y' 或 'N'")
#
#     # Part 4: select by constant dividend payout
#     while True:
#         payout = input("是否連續三年發放現金股利(Y/N): ").strip().upper()
#         if payout == "Y":
#             data = select_by_constant_dividend_payout(data)
#             break
#         elif payout == "N":
#             data = select_by_constant_dividend_payout(data)
#             break
#         else:
#             print("請輸入 'Y' 或 'N'")
#
#
#     # Part 5: select by dividend yield
#     min_yield = float(input("請輸入最小現金殖利率 (%): ")) / 100  # 轉換為小數
#     data = select_by_dividend_yield(data, min_yield)
#
#     output_csv_file = 'web_scraping_raw_data/filtered_stock_data.csv'
#     fieldnames = data[0].keys()
#
#     with open(output_csv_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
#         writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(data)
#
#     # 按照現金殖利率排序
#     data.sort(key=lambda x: float(x['現金殖利率']), reverse=True)
#
#     output_csv_file = 'web_scraping_raw_data/filtered_stock_data.csv'
#     if data:
#         fieldnames = data[0].keys()
#         with open(output_csv_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
#             writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(data)
#
#         # print(f"篩選後的股票數據已保存到 {output_csv_file}")
#         print(f"共有 {len(data)} 檔股票符合條件。")
#
#         print("\n符合條件的股票如下：")
#         print("代號, 公司名稱, 現金殖利率")
#         for row in data:
#             print(f"{row['代號']}, {row['名稱']}, {float(row['現金殖利率'])* 100: .2f}%")
#     else:
#         print("沒有符合條件的股票。")

if __name__ == '__main__':
    main()
