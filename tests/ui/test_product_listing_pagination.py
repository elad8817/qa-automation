import allure
import pytest

from src.ui.pages.product_listing_pagination_page import ProductListingPagination
from src.utils.testdata import load_json

pagination_data = load_json("pagination_assertions.json")


@pytest.fixture(scope="function", autouse=True)
def set_allure_labels():
    allure.dynamic.epic("UI testing")
    allure.dynamic.feature("Product Listing")


@pytest.fixture
def product_listing_page(driver, cfg):
    page = ProductListingPagination(driver, cfg.base_url)
    page.open()
    return page


@allure.tag("Priority: High", "Type: Positive")
@allure.id("PLP_001")
@allure.story("User can open the product listing pagination challenge page")
@allure.description("Verify total number of products in each category matches expected values")
@pytest.mark.ui
def test_product_listing_page_loads(product_listing_page):
    with allure.step("Get category labels and expected counts from page"):
        categories_name_and_counts = product_listing_page.tuple_of_categories()

    with allure.step("Check each category count across all pages"):
        for category_name, expected_count in categories_name_and_counts:
            assert product_listing_page.count_categories(category_name) == int(expected_count)
            product_listing_page.driver.refresh()


@allure.tag("Priority: High", "Type: Positive")
@allure.id("PLP_002")
@allure.story("User can find a known product in paginated listing")
@allure.description("Locate a specific product in the listing and verify it exists")
@pytest.mark.ui
def test_product_listing_contains_known_product(product_listing_page):
    with allure.step("Search for known product across paginated pages"):
        is_product_found = product_listing_page.find_product(pagination_data["sample_product"])

    with allure.step("Validate known product is present"):
        assert is_product_found


@allure.tag("Priority: Low", "Type: Positive")
@allure.id("PLP_003")
@allure.story("Pagination controls are available")
@allure.description("Validate pagination controls keep the user on product listing page")
@pytest.mark.ui
@pytest.mark.parametrize("page_number", pagination_data["pagination_pages"])
def test_pagination_controls_are_accessible(product_listing_page, page_number):
    with allure.step(f"Click specific page button: {page_number}"):
        product_listing_page.click_specific_page(page_number)

    with allure.step("Validate current url still matches listing page"):
        assert product_listing_page.current_url_contains(pagination_data["expected_page_path"])
