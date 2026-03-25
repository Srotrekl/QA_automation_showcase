"""Root conftest — sdílené fixtures pro celý projekt.

Obsahuje browser setup, Allure environment properties
a společné utility pro UI i API testy.
"""

import allure
import pytest
from playwright.sync_api import Browser, BrowserType, Playwright, sync_playwright

from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    """Spustí Playwright — session scope (1x za celý test run)."""
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser_type(playwright_instance: Playwright) -> BrowserType:
    """Vrátí BrowserType podle konfigurace (chromium/firefox/webkit)."""
    browser_name = settings.BROWSER.lower()
    logger.info("Browser: %s (headless=%s)", browser_name, settings.HEADLESS)
    return getattr(playwright_instance, browser_name)


@pytest.fixture(scope="session")
def browser(browser_type: BrowserType) -> Browser:
    """Spustí prohlížeč — session scope (1x za celý test run)."""
    import os
    slow_mo = int(os.getenv("SLOW_MO", "0"))
    browser = browser_type.launch(headless=settings.HEADLESS, slow_mo=slow_mo)
    yield browser
    browser.close()


@pytest.fixture()
def page(browser: Browser, request: pytest.FixtureRequest):
    """Vytvoří novou stránku pro každý test.

    Při selhání testu automaticky pořídí screenshot a uloží do Allure.
    """
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir="test-results/videos",
    )
    page = context.new_page()
    yield page

    # Teardown — screenshot při selhání
    if request.node.rep_call and request.node.rep_call.failed:
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=f"failure-{request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )
        logger.warning("Test FAILED: %s — screenshot uložen", request.node.name)

    page.close()
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook pro uložení výsledku testu do request.node — pro screenshot on failure."""
    import pluggy

    outcome: pluggy.Result = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
