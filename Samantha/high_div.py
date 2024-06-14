# Date: 06/13/2024
# Description: find the high dividend yield stocks listed in TWSE and OTC


def stock_pool_selection(ticker):
    '''select the stock to be included into the stock pool'''

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