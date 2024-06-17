import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Configure Firefox options
firefox_options = Options()
firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Replace with your Firefox path
firefox_options.headless = True  # Headless mode

# Initialize Firefox driver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

def get_financial_data(year, season, company_name, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            base_url = "https://mopsfin.twse.com.tw/"
            driver.get(base_url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            income_statement_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[name="IncomeStatement"]'))
            )
            driver.execute_script("arguments[0].click();", income_statement_link)
            company_id_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="輸入公司名稱或代號"]'))
            )
            company_id_input.clear()
            company_id_input.send_keys(company_name)
            compare_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.button.solid.blue.compareBtn'))
            )
            compare_btn.click()
            ys_setting_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.button.white.btn-setting.ys-setting.ysOverlay'))
            )
            driver.execute_script("arguments[0].click();", ys_setting_btn)
            setting_ys_dialog = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'setting-ys'))
            )
            year_select = setting_ys_dialog.find_element(By.ID, 'selectYear')
            year_select.send_keys(str(year))
            season_select = setting_ys_dialog.find_element(By.ID, 'selectSeason')
            season_select.send_keys(f'第{season}季')
            compare_btn2 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div[2]/a'))
            )
            compare_btn2.click()
            operating_profit_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[8]/td"))
            )
            operating_profit = operating_profit_element.text
            net_profit_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[24]/td"))
            )
            net_profit = net_profit_element.text
            return [f'{year} 第{season}季', operating_profit, net_profit]
        except Exception as e:
            retries += 1
            print(f"An error occurred: {e}. Retrying... (Attempt {retries}/{max_retries})")
            time.sleep(5)  # Wait 5 seconds before retrying
    return [f'{year} 第{season}季', 'Error', 'Error']

DATABASE_URL = "postgresql://admin:43wQoR8u75QsGMDZymTBnOTi9ce83ySS@dpg-cphhmpe3e1ms73d8lqc0-a.singapore-postgres.render.com:5432/ccclub"
engine = create_engine(DATABASE_URL)

def insert_data_to_db(data):
    try:
        with engine.begin() as connection:
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
        print(f"Successfully inserted data: {data}")
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def process_user_input():
    while True:
        try:
            year = int(input("请输入年份: "))
            season = input("请输入季度 (一, 二, 三, 四): ")
            company_name = input("请输入公司名称: ")

            try:
                data = get_financial_data(year, season, company_name)
                print(f"Retrieved data: {data}")  # Debug information
                if data[1] != 'Error' and data[2] != 'Error':  # Check if the data retrieval was successful
                    data_to_insert = data + [company_name]
                    print(f"Data to insert: {data_to_insert}")  # Print the data to be inserted
                    insert_data_to_db(data_to_insert)
                    print(f"Inserted data for {company_name}, {data[0]}")
                else:
                    print(f"Failed to retrieve valid data for {company_name}.")
            except Exception as e:
                print(f"Error processing data for {company_name}: {e}")
        except ValueError as e:
            print(f"Invalid input: {e}")
        
        more = input("Do you want to input another company? (yes/no): ").strip().lower()
        if more != 'yes':
            break

process_user_input()
driver.quit()

