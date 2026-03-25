"""Testy pro checkout flow SauceDemo.

Smoke test pokrývá kompletní E2E flow (login → add → cart → checkout → complete).
Negative testy ověřují validaci formuláře.
Regression test ověřuje správnost celkové ceny.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage


@allure.feature("Checkout")
@pytest.mark.ui
class TestCheckout:
    """Testy pro checkout flow — od přidání produktu po dokončení objednávky."""

    @pytest.mark.smoke
    def test_checkout_complete_flow(self, logged_in_page: Page) -> None:
        """Kompletní E2E flow: login → add to cart → checkout → complete.

        Procvičuje: multi-page POM, custom yield fixture (logged_in_page).
        """
        # Přidej produkt do košíku
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(index=0)
        inventory.go_to_cart()

        # Checkout
        cart = CartPage(logged_in_page)
        cart.go_to_checkout()

        checkout = CheckoutPage(logged_in_page)
        checkout.fill_checkout_info("Jan", "Testovaci", "12345")
        checkout.click_continue()

        # Dokonči objednávku
        checkout.click_finish()
        header = checkout.get_complete_header()
        assert header == "Thank you for your order!", f"Unexpected header: {header}"


@allure.feature("Checkout")
@allure.story("Validace formuláře")
@pytest.mark.negative
@pytest.mark.ui
class TestCheckoutNegative:
    """Negative testy — validace checkout formuláře s přesnými chybovými hláškami."""

    def test_checkout_missing_first_name(self, logged_in_page: Page) -> None:
        """Checkout bez jména → error 'First Name is required'."""
        self._navigate_to_checkout(logged_in_page)
        checkout = CheckoutPage(logged_in_page)
        checkout.fill_checkout_info("", "Testovaci", "12345")
        checkout.click_continue()
        error = checkout.get_error_message()
        assert "First Name is required" in error, f"Unexpected error: {error}"

    def test_checkout_missing_postal_code(self, logged_in_page: Page) -> None:
        """Checkout bez PSČ → error 'Postal Code is required'."""
        self._navigate_to_checkout(logged_in_page)
        checkout = CheckoutPage(logged_in_page)
        checkout.fill_checkout_info("Jan", "Testovaci", "")
        checkout.click_continue()
        error = checkout.get_error_message()
        assert "Postal Code is required" in error, f"Unexpected error: {error}"

    def test_checkout_missing_last_name(self, logged_in_page: Page) -> None:
        """Checkout bez příjmení → error 'Last Name is required'."""
        self._navigate_to_checkout(logged_in_page)
        checkout = CheckoutPage(logged_in_page)
        checkout.fill_checkout_info("Jan", "", "12345")
        checkout.click_continue()
        error = checkout.get_error_message()
        assert "Last Name is required" in error, f"Unexpected error: {error}"

    @staticmethod
    def _navigate_to_checkout(page: Page) -> None:
        """Helper — přidá produkt a naviguje na checkout step-one."""
        inventory = InventoryPage(page)
        inventory.add_product_to_cart(index=0)
        inventory.go_to_cart()
        cart = CartPage(page)
        cart.go_to_checkout()


@allure.feature("Checkout")
@allure.story("Cenová validace")
@pytest.mark.regression
@pytest.mark.ui
class TestCheckoutPricing:
    """Regression test — ověřuje správnost výpočtu celkové ceny."""

    def test_checkout_item_total_matches(self, logged_in_page: Page) -> None:
        """Celková cena v checkout odpovídá součtu cen přidaných produktů."""
        inventory = InventoryPage(logged_in_page)

        # Přidej 2 produkty
        inventory.add_product_to_cart(index=0)
        inventory.add_product_to_cart(index=1)
        inventory.go_to_cart()

        # Spočítej expected total z cen v košíku
        cart = CartPage(logged_in_page)
        cart_prices = cart.get_item_prices()
        expected_total = sum(cart_prices)

        # Checkout
        cart.go_to_checkout()
        checkout = CheckoutPage(logged_in_page)
        checkout.fill_checkout_info("Jan", "Testovaci", "12345")
        checkout.click_continue()

        # Ověř item total (bez daně)
        item_total = checkout.get_item_total()
        assert item_total == pytest.approx(expected_total, abs=0.01), (
            f"Item total {item_total} neodpovídá součtu cen {expected_total}"
        )
