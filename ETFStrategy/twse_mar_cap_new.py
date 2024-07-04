import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 使用 WebDriverManager 自動管理 ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 目標網頁 URL
url = 'https://www.taifex.com.tw/cht/9/futuresQADetail'

# 發送 GET 請求
driver.get(url)

# 等待頁面加載並找到表格
try:
    # 增加等待時間，並使用更可靠的定位方式
    wait = WebDriverWait(driver, 20)
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_a')))
    print("Table found successfully.")
except Exception as e:
    print(f"Failed to retrieve the table: {e}")
    driver.quit()
    exit()

# 提取表格內容
data = []
try:
    for tr in table.find_elements(By.TAG_NAME, 'tr'):
        row = []
        for td in tr.find_elements(By.TAG_NAME, 'td'):
            row.append(td.text.strip())
        if row:
            data.append(row)
    print("Table data extracted successfully.")
except Exception as e:
    print(f"Failed to extract table data: {e}")
    driver.quit()
    exit()

# 提取特定欄位資料
formatted_data = []
try:
    for row in data:
        if len(row) >= 3:  # 確保每一行至少有三個欄位
            security_name = row[0]
            market_value_ratio = row[1]
            market_ratio = row[2]
            formatted_data.append([security_name, market_value_ratio, market_ratio])
    print("Data formatted successfully.")
except Exception as e:
    print(f"Failed to format data: {e}")
    driver.quit()
    exit()

# 將資料轉成 DataFrame
try:
    df = pd.DataFrame(formatted_data, columns=['證券名稱', '市值佔大盤比重', '大盤比重'])
    df.to_csv('taifex_futures_qa.csv', index=False, encoding='utf-8-sig')
    print("CSV file 'taifex_futures_qa.csv' has been saved successfully.")
except Exception as e:
    print(f"Failed to save CSV file: {e}")
    driver.quit()
    exit()

# 關閉瀏覽器
driver.quit()
