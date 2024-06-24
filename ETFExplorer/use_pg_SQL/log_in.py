# # 获取上一级目录路径
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa: E402
# # 将上一级目录添加到 sys.path
# sys.path.insert(0, parent_dir)  # noqa: E402

# # 打印调试信息，确保路径正确
# print(f"Parent directory: {parent_dir}")  # noqa: E402
# print(f"Files in parent directory: {os.listdir(parent_dir)}")  # noqa: E402

from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
# os.chdir('C:/python-training/ccClub_InvestmentProject/aila/use_pg_SQL')
# C:\python-training\ccClub_InvestmentProject\aila\use_pg_SQL

# 6/15
# 加載 .env 文件中的環境變量
# load_dotenv()


# # 獲取環境變量
# project_dir = os.getenv('PROJECT_DIR')
# # print(f'PROJECT_DIR: {project_dir}')

# # 切換到項目目錄


# os.chdir('C:/python-training/ccClub_InvestmentProject/flask')


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
