import pandas as pd
from use_pg_SQL import log_in
import os
os.chdir('C:/python-training/ccClub_InvestmentProject/aila')
# print(os.getcwd())


def fetch_data_from_db(table):
    engine = log_in.log_in_pgSQL()
    query = f"SELECT * FROM {table}"
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df
