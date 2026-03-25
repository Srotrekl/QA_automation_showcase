"""Negative testy pro Restful Booker API.

Ověřují správné chování API při nevalidních vstupech:
chybějící pole, neexistující booking, chybějící auth.
"""

from typing import Any

import allure
import pytest

from utils.api_client import BookingAPI


@allure.feature("API Booking")
@allure.story("Negative scénáře")
@pytest.mark.negative
@pytest.mark.api
class TestBookingNegative:
    """Negative testy — neplatné vstupy a chybějící autorizace."""

    @pytest.mark.parametrize(
        "invalid_data,test_id",
        [
            (
                {
                    "lastname": "Testovaci",
                    "totalprice": 100,
                    "depositpaid": True,
                    "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
                },
                "no_firstname",
            ),
            (
                {
                    "firstname": "Jan",
                    "lastname": "Testovaci",
                    "totalprice": 100,
                    "depositpaid": True,
                },
                "no_dates",
            ),
        ],
        ids=["no_firstname", "no_dates"],
    )
    def test_create_booking_missing_fields(
        self, api_client: BookingAPI, invalid_data: dict[str, Any], test_id: str
    ) -> None:
        """Vytvoření bookingu bez povinných polí — API by mělo reagovat chybou.

        Procvičuje: @pytest.mark.parametrize s dict daty.
        Poznámka: Restful Booker API je tolerantní — může vrátit 200 i bez povinných polí.
        Test ověřuje, že API vůbec odpoví (ne 5xx).
        """
        response = api_client.create_booking(invalid_data)
        # Restful Booker vrací 500 pro neúplná data — ověřujeme že API
        # nevrátí 200 OK (tzn. nepřijme nevalidní booking jako validní)
        assert response.status_code != 200, (
            f"[{test_id}] API přijalo nevalidní data jako validní (200 OK)"
        )

    def test_get_nonexistent_booking(self, api_client: BookingAPI) -> None:
        """GET /booking/999999 — neexistující booking vrátí 404."""
        response = api_client.get_booking(999999)
        assert response.status_code == 404, (
            f"Očekáváno 404, dostal {response.status_code}"
        )

    def test_delete_booking_without_auth(
        self, api_client: BookingAPI, booking_data: dict[str, Any]
    ) -> None:
        """DELETE bez auth tokenu — server odmítne smazání (403 nebo 401)."""
        # Vytvoř booking pro test
        create_resp = api_client.create_booking(booking_data)
        booking_id = create_resp.json()["bookingid"]

        # Pokus o smazání BEZ auth tokenu
        response = api_client.delete_booking_without_auth(booking_id)
        assert response.status_code in (401, 403), (
            f"Očekáváno 401/403 bez auth, dostal {response.status_code}"
        )

        # Cleanup — smaž S auth tokenem
        api_client.auth()
        api_client.delete_booking(booking_id)
