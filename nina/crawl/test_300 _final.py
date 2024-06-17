import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd

# 配置Firefox选项
firefox_options = Options()
firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # 替换为你的Firefox安装路径
firefox_options.headless = True  # 无头模式
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument("--window-size=1920,1080")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")

# 初始化Firefox驱动
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

def get_financial_data(year, season, company_code, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            # 访问目标页面
            base_url = "https://mopsfin.twse.com.tw/"
            driver.get(base_url)
            
            # 等待页面完全加载
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            # 使用JavaScript点击综合损益表链接
            income_statement_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[name="IncomeStatement"]'))
            )
            driver.execute_script("arguments[0].click();", income_statement_link)
            
            # 查找公司代号输入框并输入公司代号
            company_id_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder=輸入公司名稱或代號]'))
            )
            company_id_input.clear()
            company_id_input.send_keys(company_code)
            
            # 查找并点击开始比较按钮
            compare_btn = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.button.solid.blue.compareBtn'))
            )
            compare_btn.click()
            
            # 等待设置按钮出现并点击
            ys_setting_btn = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.button.white.btn-setting.ys-setting.ysOverlay'))
            )
            driver.execute_script("arguments[0].click();", ys_setting_btn)
            
            # 等待 setting-ys 对话框出现
            setting_ys_dialog = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'setting-ys'))
            )
            
            # 在 setting-ys 对话框中查找年度选择框
            year_select = setting_ys_dialog.find_element(By.ID, 'selectYear')
            year_select.send_keys(str(year))
            
            # 在 setting-ys 对话框中查找季度选择框
            season_select = setting_ys_dialog.find_element(By.ID, 'selectSeason')
            season_select.send_keys(f'第{season}季')
            
            # 查找并点击开始比较按钮 (使用提供的XPath)
            compare_btn2 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div[2]/a'))
            )
            compare_btn2.click()
            
            
            # 等待包含"營業利益（損失）"的单元格加载完成
            operating_profit_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[9]/td'))
            )
            operating_profit = operating_profit_element.text
            
            # 等待包含"母公司業主（淨利∕損）"的单元格加载完成
            net_profit_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[27]/td'))
            )
            net_profit = net_profit_element.text
           

            
            return [f'{year} 第{season}季', operating_profit, net_profit]
        
        except Exception as e:
            retries += 1
            print(f"An error occurred: {e}. Retrying... (Attempt {retries}/{max_retries})")
            time.sleep(5)  # 等待5秒后重试
    
    # 如果所有重试均失败
    return [f'{year} 第{season}季', 'Error', 'Error']

DATABASE_URL = ""
engine = create_engine(DATABASE_URL)

def create_table_if_not_exists():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS f_data (
                id SERIAL PRIMARY KEY,
                季度 VARCHAR(20),
                營業利益損失 VARCHAR(50),
                母公司業主淨利損 VARCHAR(50),
                公司名稱 VARCHAR(100)
            )
        """))
        connection.commit()
def insert_data_to_db(data):
    with engine.connect() as connection:
        query = text("""
            INSERT INTO f_data (季度, 營業利益損失, 母公司業主淨利損, 公司名稱)
            VALUES (:季度, :營業利益損失, :母公司業主淨利損, :公司名稱)
        """)
        connection.execute(query, {
            '季度': data[0],
            '營業利益損失': data[1],
            '母公司業主淨利損': data[2],
            '公司名稱': data[3]
        })
        connection.commit()

create_table_if_not_exists()

# 读取CSV文件中的公司名称和代号
companies = []
with open('top_300_2.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            company_name = row[2].replace("=", "").replace('"', "") # 假设公司名称在第二列(B)
            company_code = row[1].replace("=", "").replace('"', "")
            companies.append((company_name, company_code))
        except ValueError:
            print(f"Skipping row: {row} (incorrect number of columns)")
            continue

# 准备要搜索的年份和季度
periods = [
    (2023, "一"), (2023, "二"), (2023,"三"), (2023, "四"),
    (2024, "一")
]

# 主循环
for company_name, company_code in companies:
    for year, season in periods:
        data = get_financial_data(year, season, company_code)
        data.append(company_name)  # 在数据列表中添加公司名称
        insert_data_to_db(data)  # 立即将数据插入数据库
        print(f"Inserted data for {company_name}, {year} 第{season}季")
        time.sleep(5)  # 添加短暂延迟，避免过于频繁的请求

# 关闭浏览器
driver.quit()

print("Data collection and insertion completed.")