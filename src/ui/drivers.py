from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

def create_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()

    if headless:
        # "new" is the modern headless mode in Chrome
        options.add_argument("--headless=new")

    # Stability flags for CI/Linux
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # GitHub runner path usually works automatically when chromedriver is installed
    service = ChromeService()

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver
