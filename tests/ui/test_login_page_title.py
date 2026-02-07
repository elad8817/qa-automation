
import allure
import pytest

@allure.feature("UI")
@allure.story("Open base URL and validate title")
@pytest.mark.ui
def test_homepage_title(driver, cfg):
    with allure.step("Open homepage"):
        driver.get(cfg.base_url)

    with allure.step("Validate title contains expected text"):
        # the-internet homepage title is "The Internet"
        assert "The Internet" in driver.title
