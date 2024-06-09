import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(
        dbname='ccclub',
        user='帳號',
        password='密碼',
        host='host name',
        port='5432',
        client_encoding='utf-8'  # Set client encoding to utf-8
    )

# 創建游標對象
cur = conn.cursor()

# 執行 SQL 查詢（注意欄位名稱的引號）
cur.execute('SELECT 公司代號, "營業收入-當月營收" FROM twse_data')

# 獲取所有結果
rows = cur.fetchall()

# 分離公司代號和營業收入
company_codes = [row[0] for row in rows]
revenues = [row[1] for row in rows]

# 按營業收入降序排序
sorted_data = sorted(zip(company_codes, revenues), key=lambda x: x[1], reverse=True)
company_codes, revenues = zip(*sorted_data)

# 只顯示前20家公司
company_codes = company_codes[:20]
revenues = revenues[:20]

# 繪製柱狀圖
plt.figure(figsize=(12, 8))
plt.bar(range(len(company_codes)), revenues)
plt.xlabel('公司（按營業收入降序）')
plt.ylabel('營業收入-當月營收（對數刻度）')
plt.title('前20家公司營業收入比較')
plt.xticks(range(len(company_codes)), company_codes, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.yscale('log')  # 設置y軸為對數刻度
plt.tight_layout()
plt.show()

# 關閉游標和連接
cur.close()
conn.close()