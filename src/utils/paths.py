from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
DATA_DIR = SRC_DIR / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"