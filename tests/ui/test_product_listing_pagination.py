import allure
import pytest

from src.ui.pages.product_listing_pagination_page import ProductListingPagination


@pytest.fixture(scope="function", autouse=True)
def set_allure_labels():
    allure.dynamic.epic("UI testing")
    allure.dynamic.feature("Product Listing")


@allure.tag("Priority: Medium", "Type: Positive")
@allure.id("PLP_001")
@allure.story("User can open the product listing pagination challenge page")
@allure.description(
    "Dummy smoke test that verifies the pagination page loads successfully and user lands on expected URL path"
)
@pytest.mark.ui
def test_product_listing_page_loads(driver, cfg):
    with allure.step("Open product listing pagination page"):
        page = ProductListingPagination(driver, cfg.base_url)
        page.open()

    with allure.step("Validate user is on product listing pagination page"):
        assert page.current_url_contains(page.PATH), "Product listing pagination page URL is incorrect"


@allure.tag("Priority: Medium", "Type: Positive")
@allure.id("PLP_002")
@allure.story("User can see category cards on the first page")
@allure.description("Dummy test that checks category tuples are collected from visible cards")
@pytest.mark.ui
def test_product_listing_has_categories(driver, cfg):
    with allure.step("Open product listing pagination page"):
        page = ProductListingPagination(driver, cfg.base_url)
        page.open()

    with allure.step("Collect category tuples"):
        categories = page.tuple_of_categories()

    with allure.step("Validate at least one category card is shown"):
        assert isinstance(categories, tuple), "Categories output should be a tuple"
        assert len(categories) > 0, "No categories were found on the page"


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
