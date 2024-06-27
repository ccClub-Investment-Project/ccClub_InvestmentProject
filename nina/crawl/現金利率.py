import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# 配置
WAIT_TIME = 10
SLEEP_TIME = 2
CSV_FILENAME = 'financial_dividend_data.csv'

# 检查当前工作目录
print("Current working directory:", os.getcwd())

# 改变工作目录到包含123.csv的目录
os.chdir(r'C:\Users\chimou\Desktop\Python\123')

# 读取公司数据并调试打印
try:
    companies_df = pd.read_csv('123.csv', on_bad_lines='skip', encoding='utf-8')
    print(companies_df.head())
except FileNotFoundError as e:
    print(f"File not found: {e}")
    exit(1)
except pd.errors.ParserError as e:
    print(f"Parsing error: {e}")
    exit(1)

companies = companies_df['company'].tolist()
years = range(109, 113)

# 配置 Firefox
firefox_options = Options()
firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
firefox_options.add_argument('-headless')

def initialize_driver():
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

def fetch_financial_data(driver, company, year):
    url = "https://mops.twse.com.tw/mops/web/t164sb05"
    driver.get(url)
    
    try:
        WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.ID, "co_id")))
        
        driver.find_element(By.ID, "co_id").clear()
        driver.find_element(By.ID, "co_id").send_keys(company)
        
        select_isnew = Select(driver.find_element(By.ID, "isnew"))
        options = select_isnew.options
        select_isnew.select_by_visible_text(options[-1].text)
        
        select_season = Select(driver.find_element(By.ID, "season"))
        select_season.select_by_visible_text("4")
        
        driver.find_element(By.ID, "year").clear()
        driver.find_element(By.ID, "year").send_keys(str(year))
        
        driver.find_element(By.XPATH, "//input[@type='button' and @value=' 查詢 ']").click()
        
        WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table01 table.hasBorder")))
        
        try:
            detailed_info_button = driver.find_element(By.XPATH, "//input[@type='button' and @value='詳細資料']")
            detailed_info_button.click()
            WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table01 table.hasBorder")))
        except Exception as e:
            print(f"No '詳細資料' button for {company} in year {year}: {e}")
        
        dividend_rows = driver.find_elements(By.CSS_SELECTOR, "#table01 table.hasBorder tr")
        for row in dividend_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2 and ("發放現金股利" in cells[0].text or "支付之股利" in cells[0].text):
                return cells[1].text.strip()
        
        print(f"No dividend data found for {company} in year {year}")
        return None
    except Exception as e:
        print(f"Error fetching data for {company} in year {year}: {e}")
        return None

def save_to_csv(data_list, filename):
    df = pd.DataFrame(data_list)
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False, encoding='utf-8-sig')

def main():
    driver = initialize_driver()
    
    try:
        for company in companies:
            company_name = companies_df.loc[companies_df['company'] == company, 'name'].values[0]
            company_data = {'代號': company, '公司名稱': company_name}
            
            for year in years:
                print(f"Fetching data for company: {company}, year: {year}")
                attempt = 1
                while attempt <= 3:  # 最多尝试两次
                    dividend = fetch_financial_data(driver, company, year)
                    if dividend is not None:
                        company_data[f"{year}季"] = dividend
                        break
                    else:
                        print(f"Attempt {attempt} failed. Retrying...")
                        attempt += 1
                        time.sleep(SLEEP_TIME)
                else:
                    print(f"Failed to fetch data for {company} in year {year} after 2 attempts.")
            
            save_to_csv([company_data], CSV_FILENAME)
            print(f"Data for company {company} saved to {CSV_FILENAME}")
            time.sleep(SLEEP_TIME)
    finally:
        driver.quit()

    print(f"All data processing completed. Results saved in {CSV_FILENAME}")

if __name__ == "__main__":
    main()
