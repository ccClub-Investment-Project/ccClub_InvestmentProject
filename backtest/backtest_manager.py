from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import yfinance as yf
import re, math
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

    def load_data_yahoo(self, stock_id="0050.TW"):
        # 直接讀取yahoo數據 看數據有幾年
        df = yf.download(stock_id)
        start_date = df.index[0]
        end_date = df.index[-1] 
        
        def calculate_total_months(start_date, end_date):
            total_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
            return total_months
        # 回測總共幾個月,要來推估需要多少錢？
        self.total_months = calculate_total_months(start_date, end_date)

        # 存放data
        data = bt.feeds.PandasData(dataname=df)
        self.cerebro.adddata(data)

    def buy_period(self, amount, date=15):
        # print(f'準備幾個月的現金：{self.total_months}')
        self.amount = amount
        self.total_cash=0
        self.total_cash = self.total_months * amount        
        self.cerebro.broker.setcash(self.total_cash)
        # set strategy
        self.strategy = DollarCostAveraging
        self.cerebro.addstrategy(self.strategy, amount=amount, date=date)

        # 儲存info
        self.info = {
            "每月投資金額(元)": self.amount,
            "累績投資金額(元)": self.total_cash
        }
        return self.info

    def run(self):
        self.results = self.cerebro.run()

        logs = self.results[0].logs

        # 先記錄總共買了幾個月？
        months = len(logs)
        years = round(float(months / 12),2)
        self.info['回測範圍(年)']=years

        log_dict = []
        for log in logs:
            parts = log.split(', ')
            date = parts[0]
            message = parts[1:]
            signal, price_str, cost_str, comm_str = message[0], message[1], message[2], message[3]            
            # 使用正則表達式提取數字部分
            price = float(re.search(r"[\d\.]+", price_str).group())
            cost = float(re.search(r"[\d\.]+", cost_str).group())
            comm = float(re.search(r"[\d\.]+", comm_str).group())

            item = {
                "date": date,
                "signal": signal,
                "price": price,
                "cost": cost,
                "comm": comm
            }      
            log_dict.append(item)
        return log_dict

    def analysis(self):
        # 獲取分析結果 一個策略只會有一個result 即使很多筆數據
        strat = self.results[0]
        sharpe_ratio = strat.analyzers.sharpe.get_analysis()
        drawdown = strat.analyzers.drawdown.get_analysis()
        returns = strat.analyzers.returns.get_analysis()

        if sharpe_ratio['sharperatio'] is not None:
            ana_sharpe = round(sharpe_ratio['sharperatio'], 2)
        else:
            ana_sharpe = "數據長度不足, 無法計算"
            
        ana_drawdown = round(drawdown['max']['drawdown'], 2)
        ana_returns = round(returns['rnorm100'], 2)
        
        self.ana_results = {
            "夏普值": ana_sharpe,
            "最大回撤(%)": ana_drawdown,
            "年化報酬率(%)": ana_returns
        }
        
        return self.ana_results

          
    def plot(self):
        self.cerebro.plot(iplot=False)

    