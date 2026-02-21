# file: src/ui/pages/login_flow_page.py
from selenium.webdriver.common.by import By
from src.ui.pages.base_page import BasePage, Locator

class LoginFlowPage(BasePage):
    PATH = "/challenges/login-flow"

    # Locators
    USERNAME = (By.XPATH, "//input[@type='text']")
    PASSWORD = (By.XPATH, "//input[@type='password']")

    def enter_username(self, username: str) -> None:
        self.type(self.USERNAME, username)

    def enter_password(self, password: str) -> None:
        self.type(self.PASSWORD, password)

    def check_alert(self, role: str) -> bool:
        return self.exists((By.XPATH, f"//strong[normalize-space()='{role.upper()}']"))

    def check_error(self, error_message: str) -> bool:
         return self.exists((By.XPATH, f"//div[contains(text(),'{error_message}')]"))

    def return_dashboard_text(self) -> str:
        return self.text_of((By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 font-medium css-1o5u7u9']"))

    def click_button(self, button: str) -> None:
        self.click((By.XPATH, f"//button[normalize-space()='{button}']"))