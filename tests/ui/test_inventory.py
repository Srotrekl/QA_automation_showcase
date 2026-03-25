"""Testy pro inventory stránku SauceDemo.

Smoke testy ověřují zobrazení produktů a přidání do košíku.
Regression testy pokrývají sorting, více produktů v košíku, detail, cross-browser.
"""

import allure
import pytest
from playwright.sync_api import BrowserType, Page, Playwright

from config.settings import settings
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Inventory")
@pytest.mark.smoke
@pytest.mark.ui
class TestInventorySmoke:
    """Smoke testy — základní funkčnost inventory stránky."""

    def test_inventory_page_displays_products(self, logged_in_page: Page) -> None:
        """Po loginu se zobrazí 6 produktů na inventory stránce."""
        inventory = InventoryPage(logged_in_page)
        count = inventory.get_product_count()
        assert count == 6, f"Očekáváno 6 produktů, nalezeno {count}"

    def test_add_product_to_cart(self, logged_in_page: Page) -> None:
        """Kliknutí na 'Add to cart' přidá produkt — badge ukazuje 1."""
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(index=0)
        badge = inventory.get_cart_badge_count()
        assert badge == 1, f"Cart badge ukazuje {badge}, očekáváno 1"


@allure.feature("Inventory")
@pytest.mark.regression
@pytest.mark.ui
class TestInventoryRegression:
    """Regression testy — sorting, více produktů, detail stránka."""

    def test_sort_products_by_price_low_to_high(self, logged_in_page: Page) -> None:
        """Sorting 'Price (low to high)' — ceny jsou seřazeny vzestupně."""
        inventory = InventoryPage(logged_in_page)
        inventory.sort_products("lohi")
        prices = inventory.get_product_prices()
        assert prices == sorted(prices), f"Ceny nejsou seřazeny vzestupně: {prices}"

    def test_sort_products_by_price_high_to_low(self, logged_in_page: Page) -> None:
        """Sorting 'Price (high to low)' — ceny jsou seřazeny sestupně."""
        inventory = InventoryPage(logged_in_page)
        inventory.sort_products("hilo")
        prices = inventory.get_product_prices()
        assert prices == sorted(prices, reverse=True), f"Ceny nejsou seřazeny sestupně: {prices}"

    def test_sort_products_by_name_z_to_a(self, logged_in_page: Page) -> None:
        """Sorting 'Name (Z to A)' — jména jsou seřazena sestupně."""
        inventory = InventoryPage(logged_in_page)
        inventory.sort_products("za")
        names = inventory.get_product_names()
        assert names == sorted(names, reverse=True), f"Jména nejsou seřazena sestupně: {names}"

    def test_add_multiple_products_to_cart(self, logged_in_page: Page) -> None:
        """Přidání 3 produktů do košíku — badge ukazuje 3."""
        inventory = InventoryPage(logged_in_page)
        for i in range(3):
            inventory.add_product_to_cart(index=i)
        badge = inventory.get_cart_badge_count()
        assert badge == 3, f"Cart badge ukazuje {badge}, očekáváno 3"

    def test_product_detail_page(self, logged_in_page: Page) -> None:
        """Klik na produkt otevře detail stránku s popisem a cenou."""
        inventory = InventoryPage(logged_in_page)
        first_product_name = inventory.get_product_names()[0]
        inventory.click_product(first_product_name)
        # Detail stránka má jiný URL pattern
        assert "inventory-item" in logged_in_page.url
        # Zpět na inventory
        logged_in_page.go_back()
        assert "inventory.html" in logged_in_page.url


@allure.feature("Inventory")
@allure.story("Cross-browser")
@pytest.mark.regression
@pytest.mark.ui
class TestInventoryCrossBrowser:
    """Cross-browser test — ověřuje inventory na Chromium i Firefox.

    Procvičuje: parametrizace přes prohlížeče, nezávislý browser lifecycle.
    """

    @pytest.mark.parametrize("browser_name", ["chromium", "firefox"])
    def test_inventory_cross_browser(self, playwright_instance: Playwright, browser_name: str) -> None:
        """Inventory stránka zobrazí 6 produktů na Chromium i Firefox."""
        browser_type: BrowserType = getattr(playwright_instance, browser_name)
        browser = browser_type.launch(headless=settings.HEADLESS)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        try:
            # Login
            login = LoginPage(page)
            login.open()
            login.login(settings.UI_USERNAME, settings.UI_PASSWORD)
            page.wait_for_url("**/inventory.html")

            # Ověření
            inventory = InventoryPage(page)
            count = inventory.get_product_count()
            assert count == 6, f"[{browser_name}] Očekáváno 6 produktů, nalezeno {count}"
        finally:
            context.close()
            browser.close()
