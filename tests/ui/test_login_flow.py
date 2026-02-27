import allure
import pytest

from src.ui.pages.login_flow_page import LoginFlowPage
from src.utils.testdata import load_json

users_data = load_json("users.json")
login_data = load_json("login_assertions.json")


VALID_USERS = users_data["Valid_users"]
INVALID_USERS = users_data["Invalid_users"]
ADMIN_CREDENTIALS = next(user for user in VALID_USERS if user["username"] == "admin")
STANDARD_USER_CREDENTIALS = next(user for user in VALID_USERS if user["username"] == "user")


@pytest.fixture(scope="function", autouse=True)
def set_allure_labels():
    allure.dynamic.epic("UI testing")
    allure.dynamic.feature("User Authentication System")


@pytest.fixture
def login_page(driver, cfg):
    page = LoginFlowPage(driver, cfg.base_url)
    page.open()
    return page


def login_with_credentials(page: LoginFlowPage, credentials: dict[str, str]) -> None:
    page.enter_username(credentials["username"])
    page.enter_password(credentials["password"])
    page.click_button("Login")


@allure.tag("Priority: High", "Type: Negative")
@allure.id("LF_001")
@allure.story("User will be prompted to enter credentials if they attempt to login without providing them")
@allure.description("This test verifies that if a user tries to login without entering username and password, an appropriate error message is displayed")
@pytest.mark.ui
def test_login_without_credentials(login_page):
    with allure.step("Click login button"):
        login_page.click_button("Login")

    with allure.step("Validate required fields error is shown"):
        assert login_page.check_error(login_data["errors"]["required_fields"])


@allure.tag("Priority: High", "Type: Negative")
@allure.id("LF_002")
@allure.story("User quickly realizes that they have entered incorrect credentials and is prompted with an error message")
@allure.description("This test verifies that if a user enters invalid credentials, an appropriate error message is displayed")
@pytest.mark.ui
@pytest.mark.parametrize("credentials", INVALID_USERS)
def test_login_invalid_credentials(login_page, credentials):
    with allure.step(f"Enter invalid credentials: {credentials['username']}"):
        login_with_credentials(login_page, credentials)

    with allure.step("Validate invalid credentials error is shown"):
        assert login_page.check_error(login_data["errors"]["invalid_credentials"])


@allure.tag("Priority: High", "Type: Positive")
@allure.id("LF_003")
@allure.story("User successfully logs in with valid credentials and is directed to the appropriate dashboard based on their role")
@allure.description("This test verifies that when a user enters valid credentials, they are successfully logged in and directed to the correct dashboard based on their role (User)")
@pytest.mark.ui
def test_login_user_credentials(login_page):
    with allure.step("Enter user credentials"):
        login_with_credentials(login_page, STANDARD_USER_CREDENTIALS)

    with allure.step("Validate user dashboard and role"):
        assert login_page.return_dashboard_text() == login_data["dashboards"]["user"]
        assert login_page.check_alert(login_data["roles"]["user"])


@allure.tag("Priority: High", "Type: Positive")
@allure.id("LF_004")
@allure.story("User successfully logs in with valid credentials and is directed to the appropriate dashboard based on their role")
@allure.description("This test verifies that when a user enters valid credentials, they are successfully logged in and directed to the correct dashboard based on their role (Admin)")
@pytest.mark.ui
def test_login_flow_admin(login_page):
    with allure.step("Enter admin credentials"):
        login_with_credentials(login_page, ADMIN_CREDENTIALS)

    with allure.step("Validate admin dashboard and role"):
        assert login_page.return_dashboard_text() == login_data["dashboards"]["admin"]
        assert login_page.check_alert(login_data["roles"]["admin"])


@allure.tag("Priority: High", "Type: Positive")
@allure.id("LF_005")
@allure.story("User able to logout successfully and is returned to the login page")
@allure.description("This test verifies that after a user logs in successfully, they can click the logout button and are returned to the login page with the session cleared")
@pytest.mark.ui
@pytest.mark.parametrize("credentials", VALID_USERS)
def test_login_logout(login_page, credentials):
    with allure.step(f"Login with valid credentials: {credentials['username']}"):
        login_with_credentials(login_page, credentials)

    with allure.step("Validate user role alert appears"):
        assert login_page.check_alert(login_data["roles"]["admin"]) or login_page.check_alert(login_data["roles"]["user"])

    with allure.step("Click logout button"):
        login_page.click_button("Logout")

    with allure.step("Validate session is cleared"):
        assert login_page.wait_clickable(login_page.USERNAME).get_attribute("value") == ""
        assert login_page.wait_clickable(login_page.PASSWORD).get_attribute("value") == ""
