import pandas as pd
from sqlalchemy import create_engine
import log_in

# 讀取CSV檔案
file_path = "visualize_test/taiwan_stock_index_10y.csv"
df = pd.read_csv(file_path)

# 檢查讀取的資料
print(df.head())

# 連接到資料庫
engine = log_in.log_in_pgSQL()

# 創建表格
create_table_query = """
CREATE TABLE IF NOT EXISTS taiwan_stock_index_10y (
    date DATE PRIMARY KEY,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    adj_close NUMERIC,
    volume NUMERIC
)
"""
try:
    with engine.connect() as conn:
        conn.execute(create_table_query)
        conn.commit()
    print("表格創建成功")
except Exception as e:
    print(f"創建表格時發生錯誤: {e}")

# 插入資料
try:
    df.to_sql('taiwan_stock_index_10y', engine,
              if_exists='append', index=False)
    print("資料插入成功")
except Exception as e:
    print(f"插入資料時發生錯誤: {e}")
