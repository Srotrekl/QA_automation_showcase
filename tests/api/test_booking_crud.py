"""Testy pro CRUD operace nad bookings — Restful Booker API.

Pokrývají kompletní CRUD lifecycle: Create, Read, Update, Delete.
Plus JSON schema validace, response time test a data-driven test.
"""

import json
from pathlib import Path
from typing import Any

import allure
import pytest
from jsonschema import validate

from utils.api_client import BookingAPI


def _load_booking_data() -> list[dict[str, Any]]:
    """Načte testovací booking data z externího JSON souboru."""
    data_path = Path(__file__).parent.parent.parent / "test_data" / "bookings.json"
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)


BOOKING_DATA_FROM_FILE = _load_booking_data()

# JSON schema pro response POST /booking
BOOKING_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": {
            "type": "object",
            "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
            "properties": {
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
                "totalprice": {"type": "integer"},
                "depositpaid": {"type": "boolean"},
                "bookingdates": {
                    "type": "object",
                    "required": ["checkin", "checkout"],
                    "properties": {
                        "checkin": {"type": "string"},
                        "checkout": {"type": "string"},
                    },
                },
            },
        },
    },
}


@allure.feature("API Booking")
@allure.story("CRUD operace")
@pytest.mark.api
class TestBookingCRUD:
    """Testy pro kompletní CRUD lifecycle bookingů."""

    @pytest.mark.smoke
    def test_get_booking_ids(self, api_client: BookingAPI) -> None:
        """GET /booking vrátí neprázdný seznam booking IDs."""
        response = api_client.get_booking_ids()
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list), f"Očekáván list, dostal {type(body)}"
        assert len(body) > 0, "Seznam bookingů je prázdný"

    @pytest.mark.smoke
    def test_create_booking(self, api_client: BookingAPI, booking_data: dict[str, Any]) -> None:
        """POST /booking vytvoří nový booking a vrátí ID."""
        response = api_client.create_booking(booking_data)
        assert response.status_code == 200
        body = response.json()
        assert "bookingid" in body, f"Response neobsahuje bookingid: {body}"
        assert body["booking"]["firstname"] == booking_data["firstname"]

        # Cleanup — smaž vytvořený booking
        api_client.auth()
        api_client.delete_booking(body["bookingid"])

    @pytest.mark.regression
    def test_get_booking_by_id(
        self, api_client: BookingAPI, created_booking: tuple[int, dict[str, Any]]
    ) -> None:
        """GET /booking/:id vrátí správná data vytvořeného bookingu."""
        booking_id, expected = created_booking
        response = api_client.get_booking(booking_id)
        assert response.status_code == 200
        body = response.json()
        assert body["firstname"] == expected["firstname"]
        assert body["lastname"] == expected["lastname"]
        assert body["totalprice"] == expected["totalprice"]

    @pytest.mark.regression
    def test_update_booking(
        self, api_client: BookingAPI, auth_token: str, created_booking: tuple[int, dict[str, Any]]
    ) -> None:
        """PUT /booking/:id aktualizuje booking — změní firstname."""
        booking_id, original = created_booking
        updated_data = {**original, "firstname": "Updated"}
        response = api_client.update_booking(booking_id, updated_data)
        assert response.status_code == 200
        body = response.json()
        assert body["firstname"] == "Updated"

    @pytest.mark.regression
    def test_delete_booking(
        self, api_client: BookingAPI, auth_token: str, booking_data: dict[str, Any]
    ) -> None:
        """DELETE /booking/:id smaže booking — GET pak vrátí 404."""
        # Vytvoř booking pro smazání
        create_resp = api_client.create_booking(booking_data)
        booking_id = create_resp.json()["bookingid"]

        # Smaž
        delete_resp = api_client.delete_booking(booking_id)
        assert delete_resp.status_code == 201  # Restful Booker vrací 201 pro delete

        # Ověř že booking neexistuje
        get_resp = api_client.get_booking(booking_id)
        assert get_resp.status_code == 404

    @pytest.mark.regression
    def test_create_booking_response_schema(
        self, api_client: BookingAPI, booking_data: dict[str, Any]
    ) -> None:
        """Response POST /booking odpovídá definovanému JSON schématu."""
        response = api_client.create_booking(booking_data)
        assert response.status_code == 200
        # jsonschema.validate vyhodí ValidationError pokud schema nesedí
        validate(instance=response.json(), schema=BOOKING_RESPONSE_SCHEMA)

        # Cleanup
        api_client.auth()
        api_client.delete_booking(response.json()["bookingid"])

    @pytest.mark.regression
    def test_booking_response_time(self, api_client: BookingAPI) -> None:
        """GET /booking odpovídá do 2000 ms — základní performance check."""
        response = api_client.get_booking_ids()
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert elapsed_ms < 2000, f"Response time {elapsed_ms:.0f} ms překročil limit 2000 ms"


@allure.feature("API Booking")
@allure.story("Data-driven testy")
@pytest.mark.regression
@pytest.mark.api
class TestBookingDataDriven:
    """Data-driven testy — testovací data načtená z externího JSON souboru.

    Procvičuje: @pytest.mark.parametrize + oddělení dat od logiky.
    """

    @pytest.mark.parametrize(
        "booking",
        BOOKING_DATA_FROM_FILE,
        ids=[f"{b['firstname']}_{b['lastname']}" for b in BOOKING_DATA_FROM_FILE],
    )
    def test_create_booking_from_data_file(self, api_client: BookingAPI, booking: dict[str, Any]) -> None:
        """Vytvoří booking z každé datové sady v bookings.json a ověří response."""
        response = api_client.create_booking(booking)
        assert response.status_code == 200
        body = response.json()
        assert body["booking"]["firstname"] == booking["firstname"]
        assert body["booking"]["lastname"] == booking["lastname"]
        assert body["booking"]["totalprice"] == booking["totalprice"]

        # Cleanup
        api_client.auth()
        api_client.delete_booking(body["bookingid"])
