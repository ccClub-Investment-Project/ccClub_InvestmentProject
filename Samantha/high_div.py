# Date: 06/13/2024
# Description: find the high dividend yield stocks listed in TWSE and OTC

import csv


# def stock_pool_selection(ticker):
# '''select the stock to be included into the stock pool'''
# csv path
input_csv_file = 'web_scraping_raw_data/StockList.csv'
output_csv_file = 'web_scraping_raw_data/top_300_companies.csv'

# selected columns in header
selected_columns = [0,1,2,10,11]

# open CSV file
companies = []
with open(input_csv_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    headers = next(reader)

    # selected header
    selected_headers = [headers[i] for i in selected_columns]
    print(selected_headers)


    # read every line
    for line in reader:
        selected_line = [line[i] for i in selected_columns]
        companies.append(selected_line)

    # sort by market cap
    top_300_companies = sorted(companies, key=lambda x: x[1], reverse=True)[:300]

    # write into new csv
    with open(output_csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(selected_headers)
        writer.writerows(top_300_companies)

    print(f"top 300 companies by market cap were written into {output_csv_file}")





def top_mar_cap_check(ticker):
    '''Market cap check: top 300 by market cap 市值前300大'''

def liquility_check(ticker):
    '''Liquidity check: the average daily trading volume reaches 100 million 每日平均成交額達1億'''

def earnings_check(ticker):
    '''Financial check: the sum of operating income trailing four seasons is positive 近四季營業利益總和為正數'''


def dividend_continuity_check(ticker):
    '''dividend check: consistently paid cash dividends in each of the 3 fiscal years'''


def calculate_div_yield(ticker):
    '''The forcast dividend yield can be calculated as
       1) dividend from FY23/stock price, or
       2) 最近4季EPS總和×最近3年度平均現金股利發放率 / 審核資料截止日股價'''



# main functions
def high_div_pool(ticker):
    '''generate a high dividend yield stock pool to make recommendation, ranked by dividend yield'''


def notification_announcement_rebalancing(ticker):
    '''Notifies the announcement of index rebalancing by parsing the PDF file on https://taiwanindex.com.tw/news
    '''