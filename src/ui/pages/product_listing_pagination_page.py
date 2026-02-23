from selenium.webdriver.common.by import By
from src.ui.pages.base_page import BasePage, Locator

class ProductListingPagination(BasePage):
    PATH = "/challenges/product-listing-pagination"

# Locators
    CATEGORIES_LIST_NAME = (By.XPATH, "//div[@class='bg-white border rounded-lg p-4 text-center shadow-sm hover:shadow-md transition']//p[1]")
    CATEGORIES_LIST_COUNT = (By.XPATH, "//div[@class='bg-white border rounded-lg p-4 text-center shadow-sm hover:shadow-md transition']//p[2]")
    NEXT_BUTTON = (By.XPATH, "//button[normalize-space()='Next']")
    PREV_BUTTON = (By.XPATH, "//button[normalize-space()='Prev']")


    def click_specific_page(self, page_number: int) -> None:
        self.click((By.XPATH, f"//button[normalize-space()='{page_number}']"))

    def click_next_page(self) -> None:
        self.click(self.NEXT_BUTTON)

    def click_previous_page(self) -> None:
        self.click(self.PREV_BUTTON)

    def next_page_exist(self) -> bool:
        if self.exists(self.NEXT_BUTTON):
            return True

    def count_categories(self, categorie_name) -> int:
        count = 0
        categorie_locator = (By.XPATH, f"//p[normalize-space()='Category: {categorie_name}']")
        while self.next_page_exists():
            count += len(self.driver.find_elements(*categorie_locator))
            self.click_next_page()
        return count
    def find_product(self, product_name) -> bool:
        product_locator = (By.XPATH, f"//h6[normalize-space()='{product_name}']")
        while self.next_page_exists():
            if self.exists(product_locator):
                return True
            self.click_next_page()
        return False
    def tuple_of_categories(self) -> tuple:
        categories = []
        category_elements = self.driver.find_elements(*self.CATEGORIES_LIST_NAME)
        count_elements = self.driver.find_elements(*self.CATEGORIES_LIST_COUNT)
        for name, count in zip(category_elements, count_elements):
            categories.append((name.text, count.text))
        return categories

