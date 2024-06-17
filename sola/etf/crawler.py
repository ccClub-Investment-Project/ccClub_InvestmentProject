from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Crawler():
    

    def __init__(self, remote=True, diff_container=False):

        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36' }
        
        self.remote = remote
        # 假如remote模式才考慮是不相容器下還是相同容器下
        self.diff_container = diff_container
          
        if self.diff_container:
            # 不同container 互相連線則改成容器名稱: chrome
            self.remote_url = 'http://chrome:4444/wd/hub'
        else:
            # 相同容器下的連線, 則使用localhost
            self.remote_url = 'http://localhost:4443/wd/hub'
        
        
    def configure_driver(self):
        
        options = Options()
        options.add_argument(f"user-agent={self.headers['User-Agent']}")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_argument('--headless') # 測試開發中先關閉無頭模式
        # options.add_argument("--disable-gpu")
        # options.page_load_strategy = 'none'
        # Disable sharing memory across the instances
        options.add_argument('--disable-dev-shm-usage') # 使用共享內存RAM
        # options.add_argument('--disable-gpu') # 規避部分chrome gpu bug
        # options.add_experimental_option("prefs", prefs)
        # options.add_argument('blink-settings=imagesEnabled=false') #不加載圖片提高效率
        
        # options.add_argument("--disable-site-isolation-trials")
        # options.add_argument("--disable-web-security")
        # options.add_argument("--allow-running-insecure-content")
        # options.add_argument("--disable-features=SameSiteByDefaultCookies")
        # options.add_argument("--disable-features=CookiesWithoutSameSiteMustBeSecure")
    
        if self.remote:
            # Use webdriver.Remote to connect to the Selenium Grid
            driver = webdriver.Remote(command_executor=self.remote_url, options=options)
        else:
            # Use local webdriver.Chrome (in the same container)
            driver = webdriver.Chrome(options=options)
        
        # driver.set_page_load_timeout(10)  # 設置頁面加載
        return driver
    
        