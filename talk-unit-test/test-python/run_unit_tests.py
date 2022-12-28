import sys
import pytest

# source ~/.virtualenvs/venv/bin/activate
# python run_unit_tests.py 72919259083


if __name__ == "__main__":
    params = [
        "tests/unit_tests/",
        "--cov=app",
        "--cov-report=term",
        "--cov-report=html:coverage",
        "--cov-branch",
    ]
    sys.exit(pytest.main(params))
