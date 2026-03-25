"""Centrální konfigurace projektu.

Načítá environment variables z .env souboru (lokálně)
nebo z GitHub Secrets (CI/CD). Žádné hardcoded credentials v kódu.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Konfigurace testovacího prostředí."""

    # SauceDemo — UI testy
    UI_BASE_URL: str = "https://www.saucedemo.com"
    UI_USERNAME: str = "standard_user"
    UI_PASSWORD: str = "secret_sauce"

    # Restful Booker — API testy
    API_BASE_URL: str = "https://restful-booker.herokuapp.com"
    API_USERNAME: str = "admin"
    API_PASSWORD: str = "password123"

    # Browser
    BROWSER: str = "chromium"
    HEADLESS: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


# Singleton — importuj tento objekt v celém projektu
settings = Settings()
