import backtrader as bt

class DollarCostAveraging(bt.Strategy):
    
    params = (
        ('amount', 6000),  # 每期投資金額
        ('date', 15) # 購買日期 = 觸發日期 + 1
    )

    def __init__(self):
        self.logs = []
        self.add_timer(
            when=bt.Timer.SESSION_START, # 這個觸發器是在交易日的開盤時觸發
            monthdays=[self.params.date-1],  # 每月幾號觸發,隔日購買
            monthcarry=True,  # 如果不是交易日，則延至下一個交易日
        )

    def notify_timer(self, timer, when, *args, **kwargs):
        data = self.datas[0]
        money = self.params.amount
        current_price = data.close[0]  # 获取当前数据源的收盘价
        size = money / current_price  # 计算可买入的股份数
        self.buy(data=data, size=size)

    def log(self, txt, df=None):
        '''records'''
        df = df or self.datas[0].datetime.date(0)
        content = '%s, %s' % (df.isoformat(), txt)
        self.logs.append(content)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                # self.log(f'進行定期定額投資{order.executed.price}')
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                          (order.executed.price, order.executed.value, order.executed.comm))
            elif order.issell():
                pass
                # self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        #   (order.executed.price, order.executed.value, order.executed.comm))
            self.bar_executed = len(self)
            
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            pass
            # self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade): # 交易關閉後, 處理相關資訊
        if not trade.isclosed:
            return
        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % 
                (trade.pnl, trade.pnlcomm)) # 紀錄盈利數據
