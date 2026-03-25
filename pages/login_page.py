"""Page Object pro login stránku SauceDemo.

Lokátory a akce: vyplnění přihlašovacích údajů, kliknutí na Login,
čtení chybové hlášky.
"""

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login stránka — https://www.saucedemo.com/."""

    # Lokátory
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"
    LOGO = ".login_logo"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @allure.step("Otevření login stránky")
    def open(self) -> None:
        """Naviguje na login stránku SauceDemo."""
        self.navigate("/")

    @allure.step("Login jako {username}")
    def login(self, username: str, password: str) -> None:
        """Vyplní credentials a klikne Login."""
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Vrátí text chybové hlášky (pokud je viditelná)."""
        return self.page.text_content(self.ERROR_MESSAGE) or ""

    def is_logo_visible(self) -> bool:
        """Zkontroluje jestli je logo viditelné."""
        return self.page.is_visible(self.LOGO)

    def is_username_input_visible(self) -> bool:
        """Zkontroluje jestli je username input viditelný."""
        return self.page.is_visible(self.USERNAME_INPUT)

    def is_password_input_visible(self) -> bool:
        """Zkontroluje jestli je password input viditelný."""
        return self.page.is_visible(self.PASSWORD_INPUT)

    def is_login_button_visible(self) -> bool:
        """Zkontroluje jestli je login button viditelný."""
        return self.page.is_visible(self.LOGIN_BUTTON)
