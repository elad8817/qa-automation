import allure
import pytest
import json
from src.ui.pages.login_flow_page import LoginFlowPage
from src.utils.paths import DATA_DIR


with open(DATA_DIR / "testdata.json") as f:
    test_data = json.load(f)

admin_credentials = test_data["Valid_users"][0]
user_credentials = test_data["Valid_users"][1]

@pytest.fixture(scope="function", autouse=True)
def set_allure_labels():
    allure.dynamic.epic("UI testing")
    allure.dynamic.feature("User Authentication System")

@allure.tag("Priority: High", "Type: Negative")
@allure.id("LF_001")
@allure.story("User will be prompted to enter credentials if they attempt to login without providing them")
@allure.description("This test verifies that if a user tries to login without entering username and password, an appropriate error message is displayed")
@pytest.mark.ui
def test_login_without_Credentials(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()

    with allure.step("Click login button"):
        page.click_button("Login")

    with allure.step("Validate - Error message 'Both fields are required.' is shown"):
        assert page.check_error("Both fields are required."), "Error not found, validation may have failed"



@allure.tag("Priority: High", "Type: Negative")
@allure.id("LF_002")
@allure.story("User quickly realizes that they have entered incorrect credentials and is prompted with an error message")
@allure.description("This test verifies that if a user enters invalid credentials, an appropriate error message is displayed")
@pytest.mark.ui
def test_login_invalid_credentials(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()
    for users in test_data["Invalid_users"]:
        with allure.step(f"Enter Invalid credentials: {users['username']}"):
            page.enter_username(users["username"])
            page.enter_password(users["password"])

        with allure.step("Click login button"):
            page.click_button("Login")

        with allure.step("Validate - Error message 'Invalid username or password.' is shown"):
            assert page.check_error("Invalid username or password."), "Error not found, validation may have failed"



@allure.tag("Priority: High", "Type: Positive")
@allure.id("LF_003")
@allure.story("User successfully logs in with valid credentials and is directed to the appropriate dashboard based on their role")
@allure.description("This test verifies that when a user enters valid credentials, they are successfully logged in and directed to the correct dashboard based on their role (User)")
@pytest.mark.ui
def test_login_user_credentials(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()

    with allure.step("Enter user credentials"):
        page.enter_username(user_credentials["username"])
        page.enter_password(user_credentials["password"])

    with allure.step("Click login button"):
        page.click_button("Login")

    with allure.step("Validate - User dashboard is displayed with welcome message and User role info"):
        assert page.return_dashboard_text() == "User Dashboard", "User Dashboard welcome message not found, login may have failed"
        assert page.check_alert("USER"), "User alert not found, login may have failed"


@allure.tag("Priority: High", "Type: Positive")
@allure.id("LF_004")
@allure.story("User successfully logs in with valid credentials and is directed to the appropriate dashboard based on their role")
@allure.description("This test verifies that when a user enters valid credentials, they are successfully logged in and directed to the correct dashboard based on their role (Admin)")
@pytest.mark.ui
def test_login_flow_admin(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()

    with allure.step("Enter admin credentials"):
        page.enter_username(admin_credentials["username"])
        page.enter_password(admin_credentials["password"])

    with allure.step("Click login button"):
        page.click_button("Login")

    with allure.step("Validate - Admin dashboard is displayed with welcome message and Admin role info"):
        assert page.return_dashboard_text() == "Admin Dashboard", "Admin Dashboard welcome message not found, login may have failed"
        assert page.check_alert("ADMIN"), "Admin alert not found, login may have failed"

@allure.tag("Priority: High", "Type: Positive")
@allure.id("LF_005")
@allure.story("User able to logout successfully and is returned to the login page")
@allure.description("This test verifies that after a user logs in successfully, they can click the logout button and are returned to the login page with the session cleared")
@pytest.mark.ui
def test_login_logout(driver, cfg):
    with allure.step("Open login page"):
        page = LoginFlowPage(driver, cfg.base_url)
        page.open()

    for users in test_data["Valid_users"]:
        with allure.step(f"Enter admin credentials: {users['username']}"):
            page.enter_username(users["username"])
            page.enter_password(users["password"])

        with allure.step("Click login button"):
            page.click_button("Login")

        with allure.step("Validate login result"):
            assert page.check_alert("ADMIN") or page.check_alert("USER"), "Admin/User alert not found, login may have failed"

        with allure.step("Click logout button"):
            page.click_button("Logout")

        with allure.step("Validate - Session is cleared and login form is displayed again"):
            assert page.wait_clickable(page.USERNAME).get_attribute("value") == "", "Username field not cleared after logout"
            assert page.wait_clickable(page.PASSWORD).get_attribute("value") == "", "Password field not cleared after logout"