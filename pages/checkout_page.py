"""Page Object pro checkout flow SauceDemo.

Pokrývá všechny tři kroky: checkout info → overview → complete.
"""

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Checkout stránky — step-one, step-two, complete."""

    # Step One — osobní údaje
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    ERROR_MESSAGE = "[data-test='error']"

    # Step Two — přehled objednávky
    ITEM_TOTAL = ".summary_subtotal_label"
    TAX = ".summary_tax_label"
    TOTAL = ".summary_total_label"
    FINISH_BUTTON = "[data-test='finish']"

    # Complete
    COMPLETE_HEADER = ".complete-header"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @allure.step("Vyplnění checkout údajů: {first_name} {last_name}, PSČ: {postal_code}")
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Vyplní osobní údaje na checkout step-one."""
        self.page.fill(self.FIRST_NAME_INPUT, first_name)
        self.page.fill(self.LAST_NAME_INPUT, last_name)
        self.page.fill(self.POSTAL_CODE_INPUT, postal_code)

    @allure.step("Klik na Continue")
    def click_continue(self) -> None:
        """Klikne Continue — přejde na step-two."""
        self.page.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        """Vrátí text chybové hlášky (pokud je viditelná)."""
        return self.page.text_content(self.ERROR_MESSAGE) or ""

    def get_item_total(self) -> float:
        """Vrátí subtotal cenu z overview (bez $)."""
        text = self.page.text_content(self.ITEM_TOTAL) or ""
        # Formát: "Item total: $XX.XX"
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        """Vrátí celkovou cenu (s daní) z overview."""
        text = self.page.text_content(self.TOTAL) or ""
        # Formát: "Total: $XX.XX"
        return float(text.split("$")[-1])

    @allure.step("Dokončení objednávky")
    def click_finish(self) -> None:
        """Klikne Finish — dokončí objednávku."""
        self.page.click(self.FINISH_BUTTON)

    def get_complete_header(self) -> str:
        """Vrátí text hlavičky po dokončení objednávky."""
        return self.page.text_content(self.COMPLETE_HEADER) or ""
