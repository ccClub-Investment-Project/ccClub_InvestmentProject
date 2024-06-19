from backtest_manager import BacktestManager

backtest = BacktestManager()

def one_stock(id='0050',amount=3000, date=5, duration=10):
    
    stock_ids = [f"{id}.TW"]
    buy_amount = [amount]
    buy_date = date
    duration_year = duration
    backtest.load_data_yahoo(stock_ids=stock_ids, duration_year=duration_year)
    info = backtest.buy_period(buy_amount, buy_date)
    log = backtest.run()
    analysis = backtest.analysis()
    backtest.plot()

    return (info, analysis, log)

# example
one_stock_result = one_stock("0050",3000)
print(one_stock_result[0])
print(one_stock_result[1])