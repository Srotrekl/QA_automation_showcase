"""Page Object pro inventory stránku SauceDemo.

Stránka s produkty — zobrazení, sorting, přidávání do košíku.
"""

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Inventory stránka — https://www.saucedemo.com/inventory.html."""

    # Lokátory
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    ADD_TO_CART_BUTTON = "button[data-test^='add-to-cart']"
    BURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def get_product_count(self) -> int:
        """Vrátí počet produktů na stránce."""
        return self.page.locator(self.INVENTORY_ITEM).count()

    def get_product_names(self) -> list[str]:
        """Vrátí seznam názvů všech produktů."""
        return self.page.locator(self.ITEM_NAME).all_text_contents()

    def get_product_prices(self) -> list[float]:
        """Vrátí seznam cen všech produktů (jako float, bez $)."""
        raw_prices = self.page.locator(self.ITEM_PRICE).all_text_contents()
        return [float(p.replace("$", "")) for p in raw_prices]

    @allure.step("Seřazení produktů: {option}")
    def sort_products(self, option: str) -> None:
        """Vybere sorting option z dropdown menu.

        Args:
            option: Hodnota selectu — 'az', 'za', 'lohi', 'hilo'.
        """
        self.page.select_option(self.SORT_DROPDOWN, option)

    @allure.step("Přidání produktu #{index} do košíku")
    def add_product_to_cart(self, index: int = 0) -> None:
        """Klikne na 'Add to cart' u produktu na daném indexu."""
        buttons = self.page.locator(self.ADD_TO_CART_BUTTON)
        buttons.nth(index).click()

    def get_cart_badge_count(self) -> int:
        """Vrátí číslo na cart badge (0 pokud badge neexistuje)."""
        badge = self.page.locator(self.CART_BADGE)
        if badge.is_visible():
            return int(badge.text_content() or "0")
        return 0

    @allure.step("Přechod do košíku")
    def go_to_cart(self) -> None:
        """Klikne na ikonu košíku."""
        self.page.click(self.CART_LINK)

    @allure.step("Klik na produkt: {name}")
    def click_product(self, name: str) -> None:
        """Klikne na produkt podle názvu — otevře detail."""
        self.page.locator(self.ITEM_NAME, has_text=name).click()

    @allure.step("Logout")
    def logout(self) -> None:
        """Otevře burger menu a klikne Logout."""
        self.page.click(self.BURGER_MENU)
        self.page.click(self.LOGOUT_LINK)
