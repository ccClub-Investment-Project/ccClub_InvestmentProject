import os
import getdata
import pandas as pd
from sqlalchemy import create_engine, text
from tqdm import tqdm
import log_in


def infer_sqlalchemy_type(column):
    if pd.api.types.is_integer_dtype(column):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(column):
        return 'FLOAT'
    elif pd.api.types.is_datetime64_any_dtype(column):
        return 'TIMESTAMP'
    elif pd.api.types.is_bool_dtype(column):
        return 'BOOLEAN'
    else:
        return 'VARCHAR'


table = 'financial_data'
# 讀取CSV檔案
file_path = f"C:/python-training/ccClub_InvestmentProject/aila/visualize_test/{table}.csv"
df = pd.read_csv(file_path)

# 檢查讀取的資料
print(df.head())
print(df.dtypes)

# 生成SQL表格創建語句
create_table_query = f"CREATE TABLE IF NOT EXISTS {table} (\n"

for column_name, column_type in df.dtypes.items():
    sql_type = infer_sqlalchemy_type(df[column_name])
    create_table_query += f'    "{column_name}" {sql_type},\n'

# 去掉最後一個逗號並添加結束括號
create_table_query = create_table_query.rstrip(",\n") + "\n);"

print(create_table_query)

# 連接到資料庫
engine = log_in.log_in_pgSQL()

# 創建表格
try:
    with engine.connect() as conn:
        conn.execute(text(create_table_query))
    print("表格創建成功")
except Exception as e:
    print(f"創建表格時發生錯誤: {e}")

# 插入資料
try:
    df.to_sql(table, engine, if_exists='append',
              index=False, method='multi')
    print("資料插入成功")
except Exception as e:
    print(f"插入資料時發生錯誤: {e}")

os.chdir('C:/python-training/ccClub_InvestmentProject/aila')
print(os.getcwd())

# 從資料庫讀取數據
df = getdata.fetch_data_from_db(table)

# 檢查讀取的資料
print(df)
