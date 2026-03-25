"""Testy pro login stránku SauceDemo.

Smoke testy ověřují základní přihlášení a viditelnost elementů.
Negative testy ověřují správné chybové hlášky.
Regression test ověřuje logout flow.
"""

import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from config.settings import settings
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def _load_invalid_credentials() -> list[dict]:
    """Načte neplatné credentials z test_data/users.json pro parametrizaci."""
    data_path = Path(__file__).parent.parent.parent / "test_data" / "users.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    return data["invalid_credentials"]


# Načtení dat pro parametrizovaný test — data-driven přístup
INVALID_CREDENTIALS = _load_invalid_credentials()


@allure.feature("Login")
@allure.story("Úspěšný login")
@pytest.mark.smoke
@pytest.mark.ui
class TestLoginSmoke:
    """Smoke testy — ověřují že login funguje."""

    def test_login_standard_user(self, login_page: LoginPage) -> None:
        """Úspěšný login standard_user → redirect na inventory stránku."""
        login_page.login(settings.UI_USERNAME, settings.UI_PASSWORD)
        login_page.wait_for_url("**/inventory.html")
        assert "/inventory.html" in login_page.page.url

    def test_login_page_elements_visible(self, login_page: LoginPage) -> None:
        """Všechny elementy login stránky jsou viditelné — logo, inputy, button."""
        assert login_page.is_logo_visible(), "Logo není viditelné"
        assert login_page.is_username_input_visible(), "Username input není viditelný"
        assert login_page.is_password_input_visible(), "Password input není viditelný"
        assert login_page.is_login_button_visible(), "Login button není viditelný"


@allure.feature("Login")
@allure.story("Neplatné přihlášení")
@pytest.mark.negative
@pytest.mark.ui
class TestLoginNegative:
    """Negative testy — ověřují správné chybové hlášky při neplatných vstupech."""

    def test_login_locked_out_user(self, login_page: LoginPage) -> None:
        """Zamčený uživatel vidí přesnou chybovou hlášku."""
        login_page.login("locked_out_user", "secret_sauce")
        error = login_page.get_error_message()
        assert error == "Epic sadface: Sorry, this user has been locked out.", f"Unexpected error: {error}"

    @pytest.mark.parametrize(
        "credentials",
        INVALID_CREDENTIALS,
        ids=[c["id"] for c in INVALID_CREDENTIALS],
    )
    def test_login_invalid_credentials(self, login_page: LoginPage, credentials: dict) -> None:
        """Parametrizovaný test — 3 kombinace špatných credentials z JSON souboru.

        Procvičuje: @pytest.mark.parametrize + data-driven přístup (data z externího souboru).
        """
        login_page.login(credentials["username"], credentials["password"])
        error = login_page.get_error_message()
        assert error == credentials["expected_error"], (
            f"Pro '{credentials['id']}': očekáváno '{credentials['expected_error']}', dostal '{error}'"
        )


@allure.feature("Login")
@allure.story("Logout")
@pytest.mark.regression
@pytest.mark.ui
class TestLogout:
    """Regression test — logout flow."""

    def test_logout(self, logged_in_page: Page) -> None:
        """Po loginu: menu → Logout → redirect zpět na login stránku."""
        inventory = InventoryPage(logged_in_page)
        inventory.logout()
        logged_in_page.wait_for_url("**/")
        assert "inventory" not in logged_in_page.url
