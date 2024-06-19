from backtest_manager import BacktestManager

backtest = BacktestManager()

def one_stock():
    stock_ids = ["0050.TW"]
    buy_amounts = [3000]
    buy_date = 5
    duration_year =10
    backtest.load_data_yahoo(stock_ids=stock_ids, duration_year=duration_year)
    info = backtest.buy_period(buy_amounts, buy_date)
    log = backtest.run()
    analysis = backtest.analysis()
    backtest.plot()

    return (info, analysis, log)

one_stock_result = one_stock()
print(one_stock_result[0])
print(one_stock_result[1])