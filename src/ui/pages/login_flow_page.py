# file: src/ui/pages/login_flow_page.py
from selenium.webdriver.common.by import By
from src.ui.pages.base_page import BasePage, Locator

class LoginFlowPage(BasePage):
    PATH = "/challenges/login-flow"

    # Locators
    USERNAME = (By.XPATH, "//input[@type='text']")
    PASSWORD = (By.XPATH, "//input[@type='password']")
    LOGIN_BTN = (By.XPATH, "//button[normalize-space()='Login']")
    ADMIN_ALERT = (By.XPATH, "//strong[normalize-space()='ADMIN']")
    USER_ALERT = (By.XPATH, "//strong[normalize-space()='USER']")
    EMPTY_ERROR = (By.XPATH, "//div[contains(text(),'Both fields are required.')]")
    INVALID_ERROR = (By.XPATH, "//div[contains(text(),'Invalid username or password.')]")
    DASHBOARD = (By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 font-medium css-1o5u7u9']")
    LOGOUT_BTN = (By.XPATH, "//button[normalize-space()='Logout']")

    def enter_username(self, username: str) -> None:
        self.type(self.USERNAME, username, clear=False)

    def enter_password(self, password: str) -> None:
        self.type(self.PASSWORD, password)

    def click_login(self) -> None:
        self.click(self.LOGIN_BTN)

    def click_logout(self) -> None:
        self.click(self.LOGOUT_BTN)