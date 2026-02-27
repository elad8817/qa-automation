from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Locator = Tuple[str, str]


@dataclass(frozen=True)
class BaseUrls:
    base_url: str

class BasePage:
    """
    Reusable Page Object base:
    - navigation
    - explicit waits
    - safe element helpers
    """

    PATH: str = "/"  # override in child pages if needed

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 15):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    @property
    def url(self) -> str:
        return f"{self.base_url}{self.PATH}"

    def open(self) -> "BasePage":
        self.driver.get(self.url)
        return self

    # ---------- Wait helpers ----------
    def wait_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_present(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def exists(self, locator: Locator) -> bool:
        try:
            self.driver.find_element(*locator)
            return True
        except Exception:
            return False

    # ---------- Element helpers ----------
    def click(self, locator: Locator) -> None:
        self.wait_clickable(locator).click()

    def type(self, locator: Locator, text: str, clear: bool = True) -> None:
        el = self.wait_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.wait_visible(locator).text.strip()

    def all(self, locator: Locator) -> list[WebElement]:
        self.wait_present(locator)
        return self.driver.find_elements(*locator)

    # ---------- Generic assertions ----------
    def title_contains(self, expected: str) -> bool:
        return expected in (self.driver.title or "")

    def current_url_contains(self, fragment: str) -> bool:
        return fragment in (self.driver.current_url or "")
