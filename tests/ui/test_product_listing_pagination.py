import allure
import pytest
import json
from src.ui.pages.product_listing_pagination_page import ProductListingPagination
from src.utils.paths import DATA_DIR

with open(DATA_DIR / "testdata.json") as f:
    test_data = json.load(f)

@pytest.fixture(scope="function", autouse=True)
def set_allure_labels():
    allure.dynamic.epic("UI testing")
    allure.dynamic.feature("Product Listing")