from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()

    if headless:
        options.add_argument("--headless=new")

    # Required for CI stability
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    try:
        # Selenium Manager will automatically locate Chrome + driver
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(e)
        driver.set_page_load_timeout(30)
    return driver
