from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
os.chdir('C:/python-training/ccClub_InvestmentProject/aila/use_pg_SQL')


def log_in_pgSQL():
    load_dotenv()  # 這行會加載 .env 文件中的所有變量

    dbname = os.getenv("pgSQL_dbname")
    user = os.getenv("pgSQL_user")
    password = os.getenv("pgSQL_password")
    host = os.getenv("pgSQL_host")
    port = os.getenv("pgSQL_port")

    # print(f'pgSQL_dbname: {dbname}')
    # print(f'pgSQL_user: {user}')
    # print(f'pgSQL_password: {password}')
    # print(f'pgSQL_host: {host}')
    # print(f'pgSQL_port: {port}')

    if not all([dbname, user, password, host, port]):
        raise ValueError("One or more environment variables are missing.")

    print(f"Connecting to database at {host} with user {user}")

    # 使用 SQLAlchemy 創建連接字符串
    conn_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    engine = create_engine(conn_str, client_encoding='utf8')

    print('Log in successful')
    return engine


# 測試連接
if __name__ == "__main__":
    log_in_pgSQL()
