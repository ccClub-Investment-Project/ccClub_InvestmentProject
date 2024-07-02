import csv , os
import logging
import pandas as pd

class ETFStrategy:

    def __init__(self) -> None:
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.file_name = 'stock_data_final.csv'
        self.df_csv = self.read_csv(self.get_path())
        self.df_filtered = self.df_csv.copy()
    
    # 檢查是否資料為空
    def check_empty(self, df):
        # Check if DataFrame is empty
        if df.empty:
            logging.info("The DataFrame is empty.")
    
    # log格式
    def log_filtering_info(self, df_before, df_after, condition):
        logging.info(f"Before/After filter by {condition}: {len(df_before)}/{len(df_after)} Stocks")

    # 取得路徑
    def get_path(self):
        # 獲取當前模組的目錄
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_csv_file = os.path.join(current_dir, self.file_name)
        return input_csv_file

    # 讀取 CSV 文件 (回傳dataframe)
    def read_csv(self, file_path):
        return pd.read_csv(file_path, encoding='utf-8-sig')

    # filter 01.根據市值篩選股票
    def select_by_market_cap(self, min_market_cap=400):
        df = self.df_filtered
        self.check_empty(df)
        try:
            df['市值(億)'] = df['市值(億)'].astype(float)
            filtered_df = df[df['市值(億)'] >= min_market_cap]
            self.log_filtering_info(self.df_filtered, filtered_df, f'with market cap >= {min_market_cap} 億元')
            self.df_filtered = filtered_df
        except ValueError as e:
            logging.error(f"Error converting '市值(億)' to float: {e}")

    # filter 02.根據交易量篩選股票
    def select_by_trading_volume(self, min_trading_volume=1):
        df = self.df_filtered
        self.check_empty(df)
        try:
            df['平均日成交額(元)'] = df['平均日成交額(元)'].astype(float)
            filtered_df = df[df['平均日成交額(元)'] / 100000000 >= min_trading_volume]
            self.log_filtering_info(self.df_filtered, filtered_df, f'trading volume >= {min_trading_volume} 億元')
            self.df_filtered = filtered_df
        except ValueError as e:
            logging.error(f"Error converting '平均日成交額(元)' to float: {e}")

    # filter 03.根據淨利潤篩選股票
    def select_by_profit(self, column_name = "2023年淨利", threhold = 0):
        try:
            # 将 '2023年淨利' 列转换为浮点数并进行筛选
            self.df_filtered[column_name] = self.df_filtered[column_name].astype(float)
            filtered_df = self.df_filtered[self.df_filtered[column_name] > 0]
            self.log_filtering_info(self.df_filtered, filtered_df, f'profit in {column_name} > {threhold}元')
            self.df_filtered = filtered_df
        except ValueError as e:
            logging.error(f"Error converting {column_name} to float: {e}")

    # filter 04.根據股利發放率每年 > 0 篩選股票
    def select_by_dividend_payout(self, threhold = 0):
        try:
            # 将 '2020年股利發放率', '2021年股利發放率', '2022年股利發放率' 列转换为浮点数并进行筛选
            for year in ['2020', '2021', '2022']:
                self.df_filtered[f'{year}年股利發放率'] = self.df_filtered[f'{year}年股利發放率'].astype(float)
            
            filtered_df = self.df_filtered.dropna(subset=[f'{year}年股利發放率' for year in ['2020', '2021', '2022']])
            filtered_df = filtered_df[(filtered_df['2020年股利發放率'] > threhold) & 
                                      (filtered_df['2021年股利發放率'] > threhold) & 
                                      (filtered_df['2022年股利發放率'] > threhold)]
            
            self.log_filtering_info(self.df_filtered, filtered_df, "dividend payout > {threhold} between 2020 and 2022")
            self.df_filtered = filtered_df
        except ValueError as e:
            logging.error(f"Error converting dividend payout rate to float: {e}")

    # filter 05.根據股利收益率篩選股票
    def select_by_dividend_yield(self, min_yield):
        try:
            min_yield_percent = float(min_yield) / 100
            self.df_filtered['現金殖利率'] = self.df_filtered['現金殖利率'].astype(float)            
            filtered_df = self.df_filtered[self.df_filtered['現金殖利率'] >= min_yield_percent]
            self.log_filtering_info(self.df_filtered, filtered_df, f'dividend yield >= {min_yield}')            
            self.df_filtered = filtered_df
        except ValueError as e:
            logging.error(f"Error converting '現金殖利率' to float: {e}")


