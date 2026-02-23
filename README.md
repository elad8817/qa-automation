# QA Automation Framework

A Python-based QA automation project that combines **UI testing (Selenium)** and **API testing (Requests)** with **Pytest** as the test runner and **Allure** for reporting.

Latest published Allure report: https://elad8817.github.io/qa-automation/

## What exists today

This repository currently includes:

- A reusable test framework structure under `src/`.
- UI Page Object Model foundations (`BasePage`) and an implemented `LoginFlowPage`.
- Initial API client abstraction (`ApiClient`) for REST calls.
- Working test coverage for:
  - Login flow scenarios (positive and negative) against `https://www.cnarios.com/challenges/login-flow`.
  - HTTPBin GET endpoint validation (`https://httpbin.org/get`).
- Allure integration, including automatic screenshot + page source attachment on failed UI tests.
- Configurable runtime settings via environment variables (`BASE_URL`, `API_BASE_URL`, `HEADLESS`).

## Tech stack

- Python 3.11+
- Pytest
- Selenium 4
- Requests
- Allure Pytest
- python-dotenv

## Repository structure

```text
qa-automation/
├── src/
│   ├── api/
│   │   └── client.py
│   ├── core/
│   │   └── config.py
│   ├── data/
│   │   └── testdata.json
│   ├── ui/
│   │   ├── drivers.py
│   │   └── pages/
│   │       ├── base_page.py
│   │       ├── login_flow_page.py
│   │       └── product_listing_pagination_page.py
│   └── utils/
│       └── paths.py
├── tests/
│   ├── api/
│   │   └── test_httpbin_get.py
│   ├── ui/
│   │   └── test_login_flow.py
│   └── conftest.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Getting started

### 1) Clone and enter the project

```bash
git clone <your-repo-url>
cd qa-automation
```

### 2) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows (PowerShell)
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Environment variables are read from your shell and `.env` (if present).

| Variable       | Default                   | Description |
|----------------|---------------------------|-------------|
| `BASE_URL`     | `https://www.cnarios.com` | Base URL for UI tests |
| `API_BASE_URL` | `https://httpbin.org`      | Base URL for API tests |
| `HEADLESS`     | `true`                     | Run browser headless (`true/false`) |

Example `.env`:

```env
BASE_URL=https://www.cnarios.com
API_BASE_URL=https://httpbin.org
HEADLESS=true
```

You can also override headless mode at runtime:

```bash
pytest --headless=false
```

## Running tests

### Run all tests

```bash
pytest
```

### Run only UI tests

```bash
pytest -m ui
```

### Run only API tests

```bash
pytest -m api
```

### Run a single test file

```bash
pytest tests/ui/test_login_flow.py
```

## Allure reporting

### Generate raw Allure results

```bash
pytest --alluredir=allure-results
```

### Open report locally

```bash
allure serve allure-results
```

> You need Allure CLI installed on your machine for `allure serve`.

## Current test coverage snapshot

### UI (`tests/ui/test_login_flow.py`)

- Login attempt with empty credentials.
- Invalid credentials scenarios (parameterized).
- Valid user login verification.
- Valid admin login verification.
- Logout flow verification (parameterized for valid users).

### API (`tests/api/test_httpbin_get.py`)

- GET endpoint query echo validation (`/get?hello=world`).

## Next suggested steps

Based on the project TODOs, logical next milestones are:

- Implement additional page objects for the remaining CNarios challenges.
- Add corresponding UI test suites for each new page object.
- Expand API coverage beyond basic GET checks (POST/negative/contract assertions).
- Add CI workflow for automated execution + artifact/report publishing.
- Add lint/type checks (e.g., Ruff, mypy) for higher maintainability.

## Notes

- This project relies on Selenium Manager to resolve Chrome/Chromedriver automatically.
- In CI environments, browser flags (`--no-sandbox`, `--disable-dev-shm-usage`) are already configured for stability.
