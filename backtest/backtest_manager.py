from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import yfinance as yf
# 讀取一些策略
from strategy.dollar_cost_averaging import DollarCostAveraging
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


class BacktestManager:
    def __init__(self, cash=100000, commission= 0.001425) -> None:
        self.cerebro = bt.Cerebro()
        self.cash = cash
        self.strategy = None
        # 添加分析器
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = "sharpe")
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name = "drawdown")
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name = "returns")

        # 預設值
        self.cerebro.broker.setcash(cash)
        self.cerebro.broker.setcommission(commission=commission)

    def load_data_yahoo(self, stock_ids=["0050.TW","0056.TW"], duration_year=10):

        # 添加yahoo數據 載入十年
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365 * duration_year)
        # 設定成月初
        start_date = datetime(start_date.year, start_date.month, 1)

        def calculate_total_months(start_date, end_date):
            # 计算两个日期之间的总月份数
            total_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
            return total_months

        # 回測總共幾個月,要來推估需要多少錢？
        self.total_months = calculate_total_months(start_date, end_date)

        # 存放data
        for stock_id in stock_ids:
            data = bt.feeds.PandasData(dataname=yf.download(stock_id, start=start_date, end=end_date))
            self.cerebro.adddata(data)

    
    def buy_period(self, amounts, date):
        # print(f'準備幾個月的現金：{self.total_months}')
        self.amounts = amounts
        num_datas = len(self.cerebro.datas)
        self.total_cash=0
        if len(amounts) == num_datas:
            # print("確認矩陣長度 is OK!")
            for amount in amounts:
                cash = self.total_months * amount
                self.total_cash = self.total_cash + cash
            # print(f"需準備總共多少錢:{self.total_cash}")
        else:
            print("輸入的陣列數量不同")
        self.cerebro.broker.setcash(self.total_cash)
        # set strategy
        self.strategy = DollarCostAveraging
        self.cerebro.addstrategy(self.strategy, amounts=amounts, date=date)

        # 儲存info
        info_target = f"每月投資金額(元):{''.join(map(str,self.amounts))}"
        info_prepare = f"累績投資金額(元):{self.total_cash}"

        self.info = (info_target, info_prepare)
        return self.info

    def run(self, i=0):
        self.results = self.cerebro.run()
        return self.results[i].logs

    def analysis(self, i=0):
        # 獲取分析結果 一個策略只會有一個result 即使很多筆數據
        self.ana_list = []
        for i, strat in enumerate(self.results):
            sharpe_ratio = strat.analyzers.sharpe.get_analysis()
            drawdown = strat.analyzers.drawdown.get_analysis()
            returns = strat.analyzers.returns.get_analysis()

            ana_sharpe = f"夏普值:{round(sharpe_ratio['sharperatio'], 2)}"
            ana_drawdown = f"最大回撤(%):{round(drawdown['max']['drawdown'], 2)}"
            ana_returns = f"年化報酬率(%):{round(returns['rnorm100'], 2)}"
            ana_results = (ana_sharpe,ana_drawdown,ana_returns)
            self.ana_list.append(ana_results)
        return self.ana_list[i]

          
    def plot(self):
        self.cerebro.plot(iplot=False)

    