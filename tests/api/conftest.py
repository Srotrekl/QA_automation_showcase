"""API-specifické fixtures.

Fixtures pro autentizaci, API klient a testovací data.
"""

from typing import Any

import pytest

from utils.api_client import BookingAPI
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Výchozí testovací booking data
SAMPLE_BOOKING: dict[str, Any] = {
    "firstname": "Jan",
    "lastname": "Testovaci",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-06-01",
        "checkout": "2026-06-10",
    },
    "additionalneeds": "Breakfast",
}


@pytest.fixture(scope="session")
def api_client() -> BookingAPI:
    """Vytvoří API klient — session scope (1x za celý test run)."""
    client = BookingAPI()
    logger.info("API klient vytvořen: %s", client.base_url)
    return client


@pytest.fixture(scope="session")
def auth_token(api_client: BookingAPI) -> str:
    """Získá auth token — session scope (1x za celý test run)."""
    response = api_client.auth()
    assert response.status_code == 200, f"Auth selhala: {response.text}"
    token = response.json()["token"]
    logger.info("Auth token získán: %s...", token[:8])
    return token


@pytest.fixture()
def booking_data() -> dict[str, Any]:
    """Vrátí kopii sample booking dat — každý test dostane čistou kopii."""
    import copy

    return copy.deepcopy(SAMPLE_BOOKING)


@pytest.fixture()
def created_booking(api_client: BookingAPI, auth_token: str, booking_data: dict[str, Any]):
    """Yield fixture — vytvoří booking, vrátí (id, data), po testu smaže.

    Procvičuje: custom fixture s yield pattern (setup → yield → teardown).
    """
    response = api_client.create_booking(booking_data)
    assert response.status_code == 200, f"Create booking selhalo: {response.text}"
    result = response.json()
    booking_id = result["bookingid"]
    logger.info("Booking vytvořen: ID=%s", booking_id)

    yield booking_id, result["booking"]

    # Teardown — smaž booking po testu
    api_client.delete_booking(booking_id)
    logger.info("Booking smazán (teardown): ID=%s", booking_id)
