"""Testy pro cart (košík) stránku SauceDemo.

Smoke test ověřuje zobrazení přidaných položek.
Regression test ověřuje odebrání položky z košíku.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@allure.feature("Cart")
@pytest.mark.ui
class TestCart:
    """Testy pro košík — přidání, zobrazení, odebrání položek."""

    @pytest.mark.smoke
    def test_cart_displays_added_items(self, logged_in_page: Page) -> None:
        """Přidané produkty se zobrazí v košíku se správnými názvy."""
        inventory = InventoryPage(logged_in_page)

        # Zapamatuj si název prvního produktu
        product_names = inventory.get_product_names()
        first_product = product_names[0]
        inventory.add_product_to_cart(index=0)
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart_items = cart.get_item_names()
        assert first_product in cart_items, (
            f"Produkt '{first_product}' není v košíku. Košík obsahuje: {cart_items}"
        )

    @pytest.mark.regression
    def test_remove_item_from_cart(self, logged_in_page: Page) -> None:
        """Odebrání položky z košíku — počet položek se sníží."""
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(index=0)
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        assert cart.get_item_count() == 1, "Košík by měl mít 1 položku"

        cart.remove_first_item()
        assert cart.get_item_count() == 0, "Košík by měl být prázdný po odebrání"
