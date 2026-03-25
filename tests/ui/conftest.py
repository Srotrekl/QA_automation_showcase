"""UI-specifické fixtures.

Fixtures pro Playwright stránky s login setupem a teardown logikou.
"""

import pytest
from playwright.sync_api import Page

from config.settings import settings
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture()
def login_page(page: Page) -> LoginPage:
    """Vrátí LoginPage — naviguje na login stránku."""
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture()
def logged_in_page(page: Page) -> Page:
    """Přihlásí uživatele a vrátí stránku na inventory.

    Yield fixture — po testu provede logout (teardown).
    Procvičuje: custom fixture s yield, setup/teardown pattern.
    """
    lp = LoginPage(page)
    lp.open()
    lp.login(settings.UI_USERNAME, settings.UI_PASSWORD)
    page.wait_for_url("**/inventory.html")
    yield page
    # Teardown — logout pokud jsme stále na SauceDemo stránce (ne na login)
    if "inventory" in page.url or "cart" in page.url or "checkout" in page.url:
        try:
            inventory = InventoryPage(page)
            inventory.logout()
        except Exception:
            pass  # Stránka mohla být zavřena nebo URL se změnilo
