from sqlalchemy import create_engine, text
import log_in

# 連接到資料庫
engine = log_in.log_in_pgSQL()

# 要刪除的表格名稱
table_name = "stock_index"

# 刪除表格
drop_table_query = text(f"DROP TABLE IF EXISTS {table_name}")

try:
    with engine.connect() as conn:
        conn.execute(drop_table_query)
        print(f"表格 {table_name} 刪除成功")
except Exception as e:
    print(f"刪除表格時發生錯誤: {e}")
