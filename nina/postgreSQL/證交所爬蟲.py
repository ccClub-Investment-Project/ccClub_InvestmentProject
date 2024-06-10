import pandas as pd
import requests
import io
import psycopg2
from sqlalchemy import create_engine

# Step 1: Download CSV data and load it into a DataFrame
url = 'https://mops.twse.com.tw/server-java/FileDownLoad'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/111.25 (KHTML, like Gecko) Chrome/99.0.2345.81 Safari/123.36'}
payload = {
    'step': '9',
    'functionName': 'show_file2',
    'filePath': '/t21/sii/',  # Change this if needed
    'fileName': 't21sc03_110_1.csv'  # Ensure this is the correct file
}

res = requests.post(url, data=payload, headers=headers)
res.encoding = 'utf8'

# Manually decode the text
decoded_text = res.content.decode('utf-8', errors='ignore')

# Load decoded text into a DataFrame
df = pd.read_csv(io.StringIO(decoded_text))

# Step 2: Process data
df = df.applymap(lambda s: str(s).replace(',', '') if isinstance(s, str) else s)  # Remove commas
df = df.set_index('公司代號')  # Set 公司代號 as index
df = df.applymap(lambda s: pd.to_numeric(s, errors='coerce') if isinstance(s, str) else s).dropna(how='all', axis=1)  # Convert to numeric

# Print first few rows of the DataFrame to verify
print(df.head())

# Step 3: Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname='ccclub',
        user='帳號',
        password='密碼',
        host='host name',
        port='5432',
        client_encoding='utf-8'  # Set client encoding to utf-8
    )
except psycopg2.Error as e:
    print(f"Error: {e.pgcode} - {e.pgerror}")
# Step 4: Create table and insert data
engine = create_engine('postgresql://帳號:密碼@host name:5432/DB name')
df.to_sql('twse_data', engine, if_exists='replace', index=True, index_label='公司代號')
    # Commit the transaction
conn.commit()

    # Close the connection
conn.close()