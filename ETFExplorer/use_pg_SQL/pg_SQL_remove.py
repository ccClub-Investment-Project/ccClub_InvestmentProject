import pandas as pd
from sqlalchemy import create_engine, text, inspect
import log_in

# 連接到資料庫
engine = log_in.log_in_pgSQL()

# 要操作的表格名稱
table_name = "financial_data"


def check_table_exists(engine, table_name):
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def get_table_data(engine, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df


def drop_table(engine, table_name):
    drop_table_query = text(f"DROP TABLE IF EXISTS {table_name}")
    try:
        with engine.begin() as conn:  # 使用 begin() 確保提交事務
            conn.execute(drop_table_query)
            print(f"表格 {table_name} 刪除成功")
    except Exception as e:
        print(f"刪除表格時發生錯誤: {e}")


try:
    # 刪除表格
    drop_table(engine, table_name)

    # 檢查表格是否存在
    if check_table_exists(engine, table_name):
        print(f"表格 {table_name} 存在。")

        # 獲取表格資料
        df = get_table_data(engine, table_name)

        if df.empty:
            print(f"表格 {table_name} 沒有資料。")
        else:
            print(f"表格 {table_name} 包含以下資料：")
            print(df.head())  # 顯示前幾行資料
            print("\n欄位資訊：")
            print(df.dtypes)  # 顯示欄位的資料型態
    else:
        print(f"表格 {table_name} 不存在。")
except Exception as e:
    print(f"查詢表格資料時發生錯誤: {e}")
