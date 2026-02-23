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

    def next_page_exists(self) -> bool:
        return self.exists(self.NEXT_BUTTON)

    def count_categories(self, category_name: str) -> int:
        category_locator = (By.XPATH, f"//p[normalize-space()='Category: {category_name}']")
        count = len(self.driver.find_elements(*category_locator))

        while self.next_page_exists():
            self.click_next_page()
            count += len(self.driver.find_elements(*category_locator))

        return count

    def find_product(self, product_name: str) -> bool:
        product_locator = (By.XPATH, f"//h6[normalize-space()='{product_name}']")
        if self.exists(product_locator):
            return True

        while self.next_page_exists():
            self.click_next_page()
            if self.exists(product_locator):
                return True

        return False

    def tuple_of_categories(self) -> tuple:
        categories = []
        category_elements = self.driver.find_elements(*self.CATEGORIES_LIST_NAME)
        count_elements = self.driver.find_elements(*self.CATEGORIES_LIST_COUNT)

        for name, count in zip(category_elements, count_elements):
            categories.append((name.text, count.text))

        return tuple(categories)
