



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


# 主函數
def main():
    input_csv_file = 'stock_data_final.csv'
    data = read_csv(input_csv_file)

    print("請輸入篩選條件：")

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
            data = select_by_constant_dividend_payout(data)
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

    output_csv_file = 'web_scraping_raw_data/filtered_stock_data.csv'
    if data:
        fieldnames = data[0].keys()
        with open(output_csv_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        # print(f"篩選後的股票數據已保存到 {output_csv_file}")
        print(f"共有 {len(data)} 檔股票符合條件。")

        print("\n符合條件的股票如下：")
        print("代號, 公司名稱, 現金殖利率")
        for row in data:
            print(f"{row['代號']}, {row['名稱']}, {float(row['現金殖利率'])* 100: .2f}%")
    else:
        print("沒有符合條件的股票。")

if __name__ == '__main__':
    main()
