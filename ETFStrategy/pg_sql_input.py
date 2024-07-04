# Date: 06/10/2024
# Description: create a table and insert data in PostgreSQL

# Import pandas and psycopg2 library
import pandas as pd
import psycopg2
from psycopg2 import sql

# Import os and dotenv package to load environment variables
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Load the environment variables
dbname = os.getenv('DBNAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')

# print(f'dbname: {dbname}')

# Preparatory step: set database connection parameters
db_params = {
    'dbname': dbname,
    'user': user,
    'password': password,
    'host': host
}


# Step 1: read CSV file via pandas package
csv_file_path = 'web_scraping_raw_data/data_20240607.csv'
df = pd.read_csv(csv_file_path)                     # df is dataframe

# Replace invalid values with None
df.replace('-', None, inplace=True)
df['殖利率(%)'] = pd.to_numeric(df['殖利率(%)'].astype(str).str.replace(',', ''), errors='coerce').fillna(0.0)
df['本益比'] = pd.to_numeric(df['本益比'].astype(str).str.replace(',', ''), errors='coerce').fillna(0.0)
df['股價淨值比'] = pd.to_numeric(df['股價淨值比'].astype(str).str.replace(',', ''), errors='coerce').fillna(0.0)


# Step 2: using psycopg2 package to connect to PostgreSQL data base
'''use connect function from psycopg2 library to establish a connection to a PostgreSQL database'''
'''unpacking the key-value pair and pass it as parameters'''
# conn represents an instance of a connection object that establishes a connection to the database
conn = psycopg2.connect(**db_params)

'''use cursors to execute SQL commands'''
''' .cursor() method is from psycopg2 library'''
# cur represents a cursor object
cur = conn.cursor()

# Step 3: create a table in the database
create_table_query = '''
CREATE TABLE IF NOT EXISTS dividend_yield_0607 (
    ticker INTEGER PRIMARY KEY,
    company_name TEXT,
    dividend_yield REAL,
    year_of_dividend INTEGER,
    pe_ratio REAL,
    pb_ratio REAL,
    year_quarter TEXT
);
'''
try:
    cur.execute(create_table_query)
    conn.commit()
    print("Create successfully!")
except Exception:
    print("Fail to create.")


# Step 4: insert the data from the CSV file into the PostgreSQL table
for index, row in df.iterrows():
    insert_query = sql.SQL("""
    INSERT INTO dividend_yield_0607 (ticker, company_name, dividend_yield, year_of_dividend, pe_ratio, pb_ratio, year_quarter)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """)
    try:
        cur.execute(insert_query, (row['證券代號'], row['證券名稱'], row['殖利率(%)'], row['股利年度'], row['本益比'], row['股價淨值比'], row['財報年/季']))
        conn.commit()
    except Exception as e:
        print(f"Failed to insert row {index}: {e}")
        conn.rollback()

cur.close()
conn.close()