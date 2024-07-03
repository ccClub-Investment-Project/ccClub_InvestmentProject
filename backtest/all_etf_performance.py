from data import api_table_data
# eg. etf_all_info, etf_domestic_nav, etf_domestic_list, etf_0050_constituents...
from backtest_manager import BacktestManager
import pandas as pd

def eft_performance():
    table_name = "etf_domestic_nav"
    df_etf_domestic_nav = api_table_data(table_name)

    df_sorted = df_etf_domestic_nav.sort_values(by='Market Cap',ascending=False)
    all_code = df_sorted['code']

    analysis_result = []
    info_result = []
    for code in all_code:
        print(code)
        backtest = BacktestManager()
        stock_id = f"{code}.TW"
        buy_amount = 6000
        buy_date = 5
        backtest.load_data_yahoo(stock_id=stock_id)
        info = backtest.buy_period(buy_amount)
        log = backtest.run()
        analysis = backtest.analysis()
        info_result.append(info)
        analysis_result.append(analysis)

    # 创建 info_result 的 DataFrame
    info_df = pd.DataFrame(info_result)
    info_df['stock_id'] = [f"{code}.TW" for code in all_code]
    info_df.set_index('stock_id', inplace=True)

    # 创建 analysis_result 的 DataFrame
    analysis_df = pd.DataFrame(analysis_result)
    analysis_df['stock_id'] = [f"{code}.TW" for code in all_code]
    analysis_df.set_index('stock_id', inplace=True)

    # 合并 info_df 和 analysis_df
    result_combined = analysis_df.join(info_df)

    # 排除回測範圍小於1的记录
    # result_filtered = result_combined[result_combined['回測範圍(年)'] >= 1]

    # 排序
    result_sorted = result_combined.sort_values(by="年化報酬率(%)", ascending=False)
    # 显示最终的 DataFrame
    # result_sorted.head(10)
    return result_sorted