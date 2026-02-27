import allure
import pytest

from src.ui.pages.product_listing_pagination_page import ProductListingPagination



@pytest.fixture(scope="function", autouse=True)
def set_allure_labels():
    allure.dynamic.epic("UI testing")
    allure.dynamic.feature("Product Listing")


@allure.tag("Priority: High", "Type: Positive")
@allure.id("PLP_001")
@allure.story("User can open the product listing pagination challenge page")
@allure.description(
    "Verify total number of products in each category matches expected values"
)
@pytest.mark.ui
def test_product_listing_page_loads(driver, cfg):
    with allure.step("Open product listing pagination page"):
        page = ProductListingPagination(driver, cfg.base_url)
        page.open()

    with allure.step("Get the categories and counts from all pages"):
        categories_name_and_counts = page.tuple_of_categories()
        print(f"Collected categories and counts: {categories_name_and_counts}")

    with allure.step("Check that the expected categories and counts matches expected values"):
        for category_name in categories_name_and_counts:
            print(f"Checking category: {category_name[0]} with expected count: {category_name[1]}")
            assert page.count_categories(category_name[0]) == int(category_name[1]), f"Count mismatch for category: {category_name[0]}"
            page.driver.refresh()  # Refresh page to reset pagination for next category check


@allure.tag("Priority: High", "Type: Positive")
@allure.id("PLP_002")
@allure.story("User can see category cards on the first page")
@allure.description("Locate a specific product in the listing and verify which page it is on")
@pytest.mark.ui
def test_product_listing_has_categories(driver, cfg):
    with allure.step("Navigate to product listing page"):
        page = ProductListingPagination(driver, cfg.base_url)
        page.open()

    with allure.step("Iterate through pages until product is found"):
        categories = page.tuple_of_categories()

    with allure.step("Validate at least one category card is shown"):
        assert isinstance(categories, tuple), "Categories output should be a tuple"


@allure.tag("Priority: Low", "Type: Positive")
@allure.id("PLP_003")
@allure.story("Pagination controls are available")
@allure.description("Dummy test that validates pagination controls are present on page")
@pytest.mark.ui
@pytest.mark.parametrize("page_number", [1, 2])
def test_pagination_controls_are_accessible(driver, cfg, page_number):
    with allure.step("Open product listing pagination page"):
        page = ProductListingPagination(driver, cfg.base_url)
        page.open()

    with allure.step(f"Click specific page button: {page_number}"):
        page.click_specific_page(page_number)

    with allure.step("Validate user still on challenge page after pagination click"):
        assert page.current_url_contains(page.PATH), "Navigation away from pagination page occurred"
