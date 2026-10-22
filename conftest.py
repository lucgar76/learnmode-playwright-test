import os

import pytest
from playwright.sync_api import Page

BASE_URL = "https://bugeater.web.app"


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Headed mode with slow_mo so steps are visible during test runs.

    Set PW_HEADLESS=1 to run without a browser window.
    """
    headless = os.environ.get("PW_HEADLESS", "0") == "1"
    return {
        "headless": headless,
        "slow_mo": 0 if headless else 300,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Set base URL and viewport for every browser context in the session."""
    return {
        **browser_context_args,
        "base_url": BASE_URL,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="function")
def page(page: Page):
    """
    Function-scoped page fixture.
    Each test gets a fresh tab; the browser session is reused across tests.
    """
    yield page
    page.close()
