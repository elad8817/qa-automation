import allure
import pytest
import json
from src.ui.pages.login_flow_page import LoginFlowPage

with open("../../src/data/testdata.json", "r") as f:
    test_data = json.load(f)

admin_credentials = test_data["Valid_users"][0]
user_credentials = test_data["Valid_users"][1]


@allure.feature("UI")
@allure.story("LF_001 - Empty fields validation")
@pytest.mark.ui
def test_login_without_Credentials(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()

    with allure.step("Click login button"):
        page.click_login()

    with allure.step("Validate - Error message 'Both fields are required.' is shown"):
        assert page.exists(page.EMPTY_ERROR), "Error not found, validation may have failed"

@allure.feature("UI")
@allure.story("LF_002 - Invalid credentials")
@pytest.mark.ui
def test_login_invalid_credentials(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()
    for users in test_data["Invalid_users"]:
        with allure.step("Enter Invalid credentials"):
            page.enter_username(users["username"])
            page.enter_password(users["password"])

        with allure.step("Click login button"):
            page.click_login()

        with allure.step("Validate - Error message 'Invalid username or password.' is shown"):
            assert page.exists(page.INVALID_ERROR), "Error not found, validation may have failed"


@allure.feature("UI")
@allure.story("LF_003 - Login as User")
@pytest.mark.ui
def test_login_user_credentials(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()

    with allure.step("Enter user credentials"):
        page.enter_username(user_credentials["username"])
        page.enter_password(user_credentials["password"])

    with allure.step("Click login button"):
        page.click_login()

    with allure.step("Validate - User dashboard is displayed with welcome message and User role info"):
        assert page.text_of(page.DASHBOARD) == "User Dashboard", "User Dashboard welcome message not found, login may have failed"
        assert page.exists(page.USER_ALERT), "User alert not found, login may have failed"


@allure.feature("UI")
@allure.story("Login flow with admin credentials")
@pytest.mark.ui
def test_login_flow_admin(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()

    with allure.step("Enter admin credentials"):
        page.enter_username(admin_credentials["username"])
        page.enter_password(admin_credentials["password"])

    with allure.step("Click login button"):
        page.click_login()

    with allure.step("Validate login result"):
        # Example: check for successful login, adjust as needed
        assert page.text_of(
            page.DASHBOARD) == "Admin Dashboard", "Admin Dashboard welcome message not found, login may have failed"
        assert page.exists(page.ADMIN_ALERT), "Admin alert not found, login may have failed"

@allure.feature("UI")
@allure.story("Login flow with admin credentials")
@pytest.mark.ui
def test_login_logout(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()

    for users in test_data["Valid_users"]:
        with allure.step("Enter admin credentials"):
            page.enter_username(users["username"])
            page.enter_password(users["password"])

        with allure.step("Click login button"):
            page.click_login()

        with allure.step("Validate login result"):
            # Example: check for successful login, adjust as needed
            assert page.exists(page.ADMIN_ALERT) or page.exists(page.USER_ALERT), "Admin/User alert not found, login may have failed"

        with allure.step("Click logout button"):
            page.click_logout()

        with allure.step("Validate logout result"):
            # Example: check for successful login, adjust as needed
            assert page.get_attribute_local(page.USERNAME, "value") == "", "Username field not cleared after logout"
            assert page.get_attribute_local(page.PASSWORD, "value") == "", "Password field not cleared after logout"