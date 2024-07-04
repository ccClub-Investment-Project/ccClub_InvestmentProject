# print_trading_volume.py
# 日期: 06/13/2024
# 描述: 列印在台灣證券交易所（TWSE）和店頭市場（OTC）上市股票的交易量數據並計算平均交易量

# Part 2: liquidity check:
'''Liquidity check: the average daily trading volume reaches 100 million 每日平均成交額達1億'''



import pandas as pd
import twstock

# CSV 文件路径
input_csv_file = 'web_scraping_raw_data/top_mar_cap_companies.csv'
output_csv_file = 'web_scraping_raw_data/output_trading_volumes.csv'
average_turnover_file = 'web_scraping_raw_data/average_turnovers.csv'

# 定义每块的大小
chunk_size = 10000  # 根据需要调整大小

# 初始化一个空的 DataFrame 来存储所有股票的交易量数据
all_trading_volumes = pd.DataFrame()

# 分块读取 CSV 文件并处理
for chunk in pd.read_csv(input_csv_file, chunksize=chunk_size):
    for ticker in chunk['代號'].astype(str):  # twstock 的股票代碼應為字串
        try:
            # 建立股票实例
            stock = twstock.Stock(ticker)

            # 从 twstock 获取数据
            stock_data = stock.fetch_from(2023, 6)

            # 将股票数据转换为 pandas DataFrame
            processed_data = []
            for data in stock_data:
                if data.turnover is None:
                    processed_data.append(data._replace(turnover=0))
                else:
                    processed_data.append(data)
            df_stock = pd.DataFrame(processed_data)

            # 添加一个字段来标识股票代码
            df_stock['ticker'] = ticker

            # 合并当前股票的数据到总的 DataFrame 中
            all_trading_volumes = pd.concat([all_trading_volumes, df_stock], ignore_index=True)

        except KeyError as e:
            print(f"Ticker: {ticker} 發生 KeyError: {e}")

# 将合并后的 DataFrame 输出为 CSV 文件
all_trading_volumes.to_csv(output_csv_file, index=False)

# 计算每个股票代码的平均交易量
average_turnovers = all_trading_volumes.groupby('ticker')['turnover'].mean().reset_index()
average_turnovers.columns = ['ticker', 'average_turnover']

# 将平均交易量数据输出为 CSV 文件
average_turnovers.to_csv(average_turnover_file, index=False)

print("完成列印並輸出交易量數據和平均交易量到 CSV 文件。")
