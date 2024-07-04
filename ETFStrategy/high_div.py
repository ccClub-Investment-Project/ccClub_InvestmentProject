# Date: 06/13/2024
# Description: find the high dividend yield stocks listed in TWSE and OTC

# Part 2: liquidity check:
'''Liquidity check: the average daily trading volume reaches 100 million 每日平均成交額達1億'''

import pandas as pd
import twstock


# csv file path
input_csv_file = 'web_scraping_raw_data/top_mar_cap_companies.csv'
output_csv_file = 'web_scraping_raw_data/top_mar_cap_companies_w_trading_volume.csv'

# read csv file
df_csv = pd.read_csv(input_csv_file)
# print(df_csv)
# print(df_csv['代號'])
# print(df_csv['代號'].astype(int))

# create a dictionary to save stock ticker and corresponding trading volume
average_volumes = {}

# calculate trading volume for corresponding stocks
for ticker in df_csv['代號'].astype(str):     # twstock's ticker should be string
    # construct a stock instance
    stock = twstock.Stock(ticker)

    # fetch data from twstock
    stock_data = stock.fetch_from(2023, 6)
    # print(stock_data)
    # print(len(stock_data))

    # transform stock data into pandas Dataframe
    processed_data = []
    for data in stock_data:
        if data.turnover is None:
            print(data.turnover)
            processed_data.append(data._replace(turnover=0))
        else:
            processed_data.append(data)
    df_stock = pd.DataFrame(processed_data)

    # [Data(date=datetime.datetime(2023, 6, 1, 0, 0), capacity=25257673, turnover=13920836412, open=550.0, high=554.0, low=550.0, close=551.0, change=-7.0, transaction=25441), ..................]

    # set the index of pandas DataFrame *****************
    # df_stock.set_index('date', inplace=True)

    average_volume = df_stock['turnover'].mean()


    # add to the dictionary of stock
    average_volume= df_stock['turnover'].mean()
    average_volumes[ticker] = average_volume

# add the trading volume to new column in csv
df_csv['240天平均成交量'] = df_stock['代號']

# save to new csv
df_csv.to_csv(output_csv_file,index=False)
# df_csv.to_csv(output_csv_file, index=False)

print(f"csv file is saved to {output_csv_file}")
