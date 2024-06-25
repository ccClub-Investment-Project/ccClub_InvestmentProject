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
CSV_FILENAME = 'financial_net_income_data.csv'

# 读取公司数据
companies_df = pd.read_csv('company.csv')
companies = companies_df['company'].tolist()
years = range(109, 113)
seasons = range(1, 5)

# 配置 Firefox
firefox_options = Options()
firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
firefox_options.add_argument('-headless')

def initialize_driver():
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

def fetch_financial_data(driver, company, year, season):
    url = f"https://mops.twse.com.tw/mops/web/t164sb04?encodeURIComponent=1&step=1&firstin=1&off=1&TYPEK=all&year={year}&season={season}&co_id={company}"
    driver.get(url)
    
    try:
        WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table01 table.hasBorder")))
        
        net_income_rows = driver.find_elements(By.CSS_SELECTOR, "#table01 table.hasBorder tr")
        for row in net_income_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2 and "母公司業主（净利／损）" in cells[0].text:
                return cells[1].text.strip()
        
        print(f"No net income data found for {company} in year {year}, season {season}")
        return None
    except Exception as e:
        print(f"Error fetching data for {company} in year {year}, season {season}: {e}")
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
                for season in seasons:
                    print(f"Fetching data for company: {company}, year: {year}, season: {season}")
                    attempt = 1
                    while attempt <= 2:  # 最多尝试两次
                        net_income = fetch_financial_data(driver, company, year, season)
                        if net_income is not None:
                            company_data[f"{year}年第{season}季"] = net_income
                            break
                        else:
                            print(f"Attempt {attempt} failed. Retrying...")
                            attempt += 1
                            time.sleep(SLEEP_TIME)
                    else:
                        print(f"Failed to fetch data for {company} in year {year}, season {season} after 2 attempts.")
            
            save_to_csv([company_data], CSV_FILENAME)
            print(f"Data for company {company} saved to {CSV_FILENAME}")
            time.sleep(SLEEP_TIME)
    finally:
        driver.quit()

    print(f"All data processing completed. Results saved in {CSV_FILENAME}")

if __name__ == "__main__":
    main()
