import pytest

from internal.common import BASE_PATH

TESTS_DIR = BASE_PATH / "tests"


def test():
    """Run browser tests with Playwright."""
    return pytest.main(TESTS_DIR)
