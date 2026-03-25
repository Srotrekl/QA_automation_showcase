"""Testy pro autentizaci Restful Booker API.

Ověřují získání tokenu a chování při neplatných credentials.
"""

import allure
import pytest

from utils.api_client import BookingAPI


@allure.feature("API Auth")
@pytest.mark.api
class TestAuth:
    """Testy autentizačního endpointu POST /auth."""

    @pytest.mark.smoke
    def test_auth_creates_token(self, api_client: BookingAPI) -> None:
        """POST /auth s validními credentials vrátí token."""
        response = api_client.auth()
        assert response.status_code == 200
        body = response.json()
        assert "token" in body, f"Response neobsahuje token: {body}"
        assert len(body["token"]) > 0, "Token je prázdný"

    @pytest.mark.negative
    def test_auth_invalid_credentials(self) -> None:
        """POST /auth se špatnými údaji vrátí 'Bad credentials'."""
        client = BookingAPI()
        response = client.auth(username="neexistujici", password="spatne_heslo")
        assert response.status_code == 200  # API vrací 200 i při chybě
        body = response.json()
        assert "reason" in body, f"Response neobsahuje 'reason': {body}"
        assert body["reason"] == "Bad credentials"
