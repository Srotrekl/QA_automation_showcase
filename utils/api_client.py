"""Wrapper nad requests pro Restful Booker API.

Zapouzdřuje HTTP volání, přidává auth token,
loguje request/response a měří response time.
"""

from typing import Any

import allure
import requests

from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BookingAPI:
    """HTTP klient pro Restful Booker API."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or settings.API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self.token: str | None = None

    @allure.step("POST /auth — získání auth tokenu")
    def auth(self, username: str | None = None, password: str | None = None) -> requests.Response:
        """Autentizace — vrátí response s tokenem."""
        payload = {
            "username": username or settings.API_USERNAME,
            "password": password or settings.API_PASSWORD,
        }
        response = self._request("POST", "/auth", json=payload)
        if "token" in response.json():
            self.token = response.json()["token"]
            self.session.cookies.set("token", self.token)
            logger.info("Auth token získán")
        return response

    @allure.step("GET /booking — seznam booking IDs")
    def get_booking_ids(self) -> requests.Response:
        """Vrátí seznam všech booking IDs."""
        return self._request("GET", "/booking")

    @allure.step("GET /booking/{booking_id}")
    def get_booking(self, booking_id: int) -> requests.Response:
        """Vrátí detail konkrétního bookingu."""
        return self._request("GET", f"/booking/{booking_id}")

    @allure.step("POST /booking — vytvoření nového bookingu")
    def create_booking(self, data: dict[str, Any]) -> requests.Response:
        """Vytvoří nový booking."""
        return self._request("POST", "/booking", json=data)

    @allure.step("PUT /booking/{booking_id} — aktualizace bookingu")
    def update_booking(self, booking_id: int, data: dict[str, Any]) -> requests.Response:
        """Aktualizuje existující booking (vyžaduje auth)."""
        return self._request("PUT", f"/booking/{booking_id}", json=data)

    @allure.step("DELETE /booking/{booking_id}")
    def delete_booking(self, booking_id: int) -> requests.Response:
        """Smaže booking (vyžaduje auth)."""
        return self._request("DELETE", f"/booking/{booking_id}")

    def delete_booking_without_auth(self, booking_id: int) -> requests.Response:
        """Pokusí se smazat booking BEZ auth tokenu — pro negative test."""
        url = f"{self.base_url}/booking/{booking_id}"
        return requests.delete(url, headers={"Content-Type": "application/json"})

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """Interní metoda — provede HTTP request, loguje a attachne do Allure."""
        url = f"{self.base_url}{path}"
        logger.info("%s %s", method, url)

        response = self.session.request(method, url, **kwargs)

        # Logování
        logger.info("Response: %s (%s ms)", response.status_code, response.elapsed.total_seconds() * 1000)

        # Allure attachment — response body
        try:
            body = response.json()
        except ValueError:
            body = response.text
        allure.attach(
            str(body),
            name=f"{method} {path} — response",
            attachment_type=allure.attachment_type.JSON,
        )

        return response
