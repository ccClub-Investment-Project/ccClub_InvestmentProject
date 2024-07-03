from consolidate2 import ETFStrategy

def strategy_basic(n=0):
    # 物件初始化 (讀取csv -> dataframe)
    etf_strategy = ETFStrategy()
    # Step 01.根據市值篩選股票 (市值 >= 400億)
    etf_strategy.select_by_market_cap(400)
    # step 02.根據交易量篩選股票 (成交量 >= 1億)
    etf_strategy.select_by_trading_volume(1)
    # step 03.根據淨利潤篩選股票 (2023年淨利 > 0)
    etf_strategy.select_by_profit('2023年淨利',0)
    # step 04.根據股利發放率篩選股票 (股利發放率 > 0%) 
    etf_strategy.select_by_dividend_payout(0)
    # 根據殖利率排序
    etf_strategy.df_filtered = etf_strategy.df_filtered.sort_values(by="現金殖利率",ascending=False)
    if n!=0:
        etf_strategy.df_filtered = etf_strategy.df_filtered.head(n)
    return etf_strategy

def strategy_yield(min_yield = 5):
    etf_strategy = strategy_basic()
    # step 05.根據股利收益率篩選股票 (殖利率 > 5%)
    etf_strategy.select_by_dividend_yield(min_yield)
    return etf_strategy

