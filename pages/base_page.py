"""Bázová třída pro všechny Page Object stránky.

Obsahuje sdílené metody — navigate, screenshot, wait.
Všechny konkrétní stránky (LoginPage, InventoryPage, ...) dědí z BasePage.
"""

import allure
from playwright.sync_api import Page

from utils.logger import setup_logger

logger = setup_logger(__name__)


class BasePage:
    """Společný základ pro všechny page objecty."""

    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Navigace na {path}")
    def navigate(self, path: str = "") -> None:
        """Otevře URL — base_url + path."""
        from config.settings import settings

        url = f"{settings.UI_BASE_URL}{path}"
        logger.info("Navigace na %s", url)
        self.page.goto(url)

    @allure.step("Screenshot: {name}")
    def take_screenshot(self, name: str) -> bytes:
        """Pořídí screenshot a vrátí bytes (pro Allure attachment)."""
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot

    def get_title(self) -> str:
        """Vrátí titulek aktuální stránky."""
        return self.page.title()

    def wait_for_url(self, url_pattern: str, timeout: float = 5000) -> None:
        """Počká než se URL změní na očekávaný pattern."""
        self.page.wait_for_url(url_pattern, timeout=timeout)
