import logging
import os
import re
from pathlib import Path

import allure
import pytest

from src.api.client import ApiClient
from src.core.config import Settings, str_to_bool
from src.ui.drivers import create_chrome_driver


TEST_LOGS_DIR = Path("test-logs")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="Run browser headless: true/false (overrides HEADLESS env var).",
    )


def pytest_configure(config):
    # Console logging (works great in CI too)
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    TEST_LOGS_DIR.mkdir(exist_ok=True)


@pytest.fixture
def test_logger(request):
    return logging.getLogger(f"test.{request.node.nodeid}")


@pytest.fixture(autouse=True)
def attach_test_logs(request, test_logger):
    node_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.nodeid)
    log_path = TEST_LOGS_DIR / f"{node_id}.log"

    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)

    test_logger.info("START test: %s", request.node.nodeid)

    yield

    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    rep_teardown = getattr(request.node, "rep_teardown", None)

    if any(rep and rep.failed for rep in (rep_setup, rep_call, rep_teardown)):
        test_logger.error(
            "END test: %s (status=failed, setup=%s, call=%s, teardown=%s)",
            request.node.nodeid,
            getattr(rep_setup, "outcome", "n/a"),
            getattr(rep_call, "outcome", "n/a"),
            getattr(rep_teardown, "outcome", "n/a"),
        )
    else:
        test_logger.info("END test: %s (status=passed)", request.node.nodeid)

    root_logger.removeHandler(file_handler)
    file_handler.close()

    if log_path.exists():
        allure.attach.file(
            str(log_path),
            name="test_log",
            attachment_type=allure.attachment_type.TEXT,
        )

    TEST_LOGS_DIR.mkdir(exist_ok=True)


@pytest.fixture(autouse=True)
def attach_test_logs(request):
    node_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.nodeid)
    log_path = TEST_LOGS_DIR / f"{node_id}.log"

    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)

    yield

    root_logger.removeHandler(file_handler)
    file_handler.close()

    if log_path.exists():
        allure.attach.file(
            str(log_path),
            name="test_log",
            attachment_type=allure.attachment_type.TEXT,
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


def _attach_failure_artifacts(drv, phase: str):
    try:
        allure.attach(
            drv.get_screenshot_as_png(),
            name=f"{phase}_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass

    try:
        allure.attach(
            drv.page_source,
            name=f"{phase}_page_source",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Attach screenshot + page source to Allure on UI test failure
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.failed and "driver" in item.fixturenames and "driver" in item.funcargs:
        _attach_failure_artifacts(item.funcargs["driver"], rep.when)
