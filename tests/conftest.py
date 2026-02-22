import allure
import pytest
from src.core.config import settings
from src.api.client import ApiClient
from src.ui.drivers import create_chrome_driver

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="Run browser in headless mode (true/false)",
    )

@pytest.fixture(scope="session")
def cfg():
    return settings

@pytest.fixture(scope="session")
def cfg(pytestconfig):
    from src.core.config import Settings

    headless_opt = pytestconfig.getoption("headless")
    if headless_opt is not None:
        headless = headless_opt
        from src.core.config import settings as orig_settings
        # Override only headless, keep other settings
        return Settings(
            base_url=orig_settings.base_url,
            api_base_url=orig_settings.api_base_url,
            headless=headless,
        )
    else:
        from src.core.config import settings
        return settings

@pytest.fixture(scope="session")
def api(cfg):
    return ApiClient(cfg.api_base_url)

@pytest.fixture
def driver(cfg):
    drv = create_chrome_driver(headless=cfg.headless)
    yield drv
    drv.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Attach screenshot + page source to Allure on UI test failure
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed and "driver" in item.fixturenames:
        drv = item.funcargs["driver"]
        try:
            allure.attach(
                drv.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass

        try:
            allure.attach(
                drv.page_source,
                name="page_source",
                attachment_type=allure.attachment_type.HTML,
            )
        except Exception:
            pass
