# 連結到SQL
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import json


load_dotenv()

dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")

import matplotlib.pyplot as plt


def log_in_pgSQL():
    # 使用 SQLAlchemy 創建連接字符串
    conn_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    engine = create_engine(conn_str, client_encoding='utf8')
    print('Log in successful')
    return engine

engine = log_in_pgSQL()



def get_json(table):
    query = f"SELECT * FROM {table}"
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
        data = df.to_json(orient='records',force_ascii=False)
        return json.loads(data)
    
# table = "etf_all_info"
# data = get_json(table)
# data_list = json.loads(data)
# print(type(data_list))
# print(data_list[0])

# # 轉乘json
# json_data = json.dumps(data_list, ensure_ascii=False)
# print(json_data)