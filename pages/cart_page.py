"""Page Object pro cart (košík) stránku SauceDemo.

Zobrazení přidaných produktů, odebrání, navigace na checkout.
"""

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    """Cart stránka — https://www.saucedemo.com/cart.html."""

    # Lokátory
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    REMOVE_BUTTON = "button[data-test^='remove']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CONTINUE_SHOPPING = "[data-test='continue-shopping']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def get_item_count(self) -> int:
        """Vrátí počet položek v košíku."""
        return self.page.locator(self.CART_ITEM).count()

    def get_item_names(self) -> list[str]:
        """Vrátí názvy všech položek v košíku."""
        return self.page.locator(self.ITEM_NAME).all_text_contents()

    def get_item_prices(self) -> list[float]:
        """Vrátí ceny všech položek v košíku (bez $)."""
        raw = self.page.locator(self.ITEM_PRICE).all_text_contents()
        return [float(p.replace("$", "")) for p in raw]

    @allure.step("Odebrání první položky z košíku")
    def remove_first_item(self) -> None:
        """Klikne na 'Remove' u první položky."""
        self.page.locator(self.REMOVE_BUTTON).first.click()

    @allure.step("Přechod na checkout")
    def go_to_checkout(self) -> None:
        """Klikne na 'Checkout' button."""
        self.page.click(self.CHECKOUT_BUTTON)

    @allure.step("Zpět na nákupy")
    def continue_shopping(self) -> None:
        """Klikne na 'Continue Shopping'."""
        self.page.click(self.CONTINUE_SHOPPING)
