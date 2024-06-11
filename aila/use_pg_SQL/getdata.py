import pandas as pd
import log_in


def fetch_data_from_db(table):
    engine = log_in.log_in_pgSQL()
    query = f"SELECT * FROM {table}"
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df
