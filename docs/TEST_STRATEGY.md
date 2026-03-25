# Test Strategy

## Scope

Automatizované testování dvou veřejných aplikací:

| Aplikace | Typ testů | Co pokrýváme |
|----------|----------|--------------|
| **SauceDemo** (saucedemo.com) | UI E2E | Login, inventory, cart, checkout |
| **Restful Booker** (restful-booker.herokuapp.com) | REST API | Auth, CRUD bookings, validace |

## Typy testů

| Typ | Marker | Účel | Počet |
|-----|--------|------|-------|
| **Smoke** | `@pytest.mark.smoke` | Rychlá kontrola po každé změně | ~8 |
| **Regression** | `@pytest.mark.regression` | Kompletní pokrytí funkcionality | ~15 |
| **Negative** | `@pytest.mark.negative` | Nevalidní vstupy, error handling | ~8 |

## Out of Scope

- Performance / load testing (mimo scope portfolia)
- Security testing (penetrační testy)
- Mobile testing
- Vizuální regresní testování (screenshot comparison)
- Testování vlastního backendu (testujeme veřejné aplikace)

## Spouštění testů

```bash
# Smoke testy — po každé změně
pytest -m smoke

# Celá regrese
pytest -m regression

# Jen API testy
pytest tests/api/

# Jen UI testy
pytest tests/ui/

# Konkrétní soubor
pytest tests/ui/test_login.py -v
```

## CI/CD

- **Trigger:** push do `main`, PR do `main`
- **Matrix:** Chromium + Firefox
- **Reporting:** Allure report jako artifact
- **Secrets:** credentials přes GitHub Secrets

## Reporting

- **Allure Report** — detailní report s kroky, screenshoty a response body
- **CI artifacts** — screenshot/video při selhání
- Generování: `pytest --alluredir=allure-results && allure serve allure-results`

## Matice pokrytí

| Funkce | Smoke | Regression | Negative |
|--------|:-----:|:----------:|:--------:|
| Login (UI) | test_login_standard_user | test_logout | test_login_locked_out_user, test_login_invalid_credentials |
| Inventory (UI) | test_inventory_page_displays_products, test_add_product_to_cart | test_sort_*, test_add_multiple_*, test_product_detail, test_cross_browser | — |
| Cart (UI) | test_cart_displays_added_items | test_remove_item_from_cart | — |
| Checkout (UI) | test_checkout_complete_flow | test_checkout_item_total_matches | test_checkout_missing_* |
| Auth (API) | test_auth_creates_token | — | test_auth_invalid_credentials |
| Booking CRUD (API) | test_get_booking_ids, test_create_booking | test_get_by_id, test_update, test_delete, test_schema, test_response_time | test_missing_fields, test_nonexistent, test_without_auth |
