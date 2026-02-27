import logging
import os

import allure
import pytest

from src.api.client import ApiClient
from src.core.config import Settings, str_to_bool
from src.ui.drivers import create_chrome_driver


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="Run browser headless: true/false (overrides HEADLESS env var).",
    )


def pytest_configure(config):
    # Console logging (works great in CI too)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


@pytest.fixture(scope="session")
def cfg(pytestconfig):
    cli_headless = pytestconfig.getoption("--headless")
    if cli_headless is not None:
        headless = str_to_bool(cli_headless)
    else:
        headless = str_to_bool(os.getenv("HEADLESS", "true"))

    return Settings(headless=headless)


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
