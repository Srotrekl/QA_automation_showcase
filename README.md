# QA Automation Showcase

[![CI](https://github.com/Srotrekl/QA_automation_showcase/actions/workflows/tests.yml/badge.svg)](https://github.com/Srotrekl/QA_automation_showcase/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-39%20passed-brightgreen)](#test-coverage)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

End-to-end UI and REST API test suite for **SauceDemo** and **Restful Booker** — pytest, Playwright, Allure reporting, Postman/Newman, CI/CD on every push.

**39 tests · UI + API · 2 browsers in CI · real bug found & documented**

---

## What this demonstrates

| Skill | How it shows up |
|---|---|
| **UI E2E testing** | Playwright + Page Object Model across login, cart, checkout flows |
| **REST API testing** | pytest + requests: auth, CRUD, negative scenarios (404, 403) |
| **Test design** | Smoke / regression / negative markers; parametrised test data from JSON |
| **Reporting** | Allure with step-level detail, screenshots on failure |
| **CI/CD** | GitHub Actions: 2-browser matrix (Chromium, Firefox), Allure artifacts |
| **Tool breadth** | Same API domain tested twice — pytest/requests + Postman/Newman |
| **Bug reporting** | Real defect found, documented with reproduction steps and severity |

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| **pytest** | 8.3.4 | Test runner, fixtures, markers |
| **Playwright** | 1.49.1 | Browser automation (Page Object Model) |
| **requests** | 2.32.3 | REST API testing |
| **Allure** | 2.13.5 | Reporting — steps, screenshots, attachments |
| **pydantic-settings** | 2.7.1 | Typed environment configuration |
| **jsonschema** | 4.23.0 | API response schema validation |
| **ruff** | 0.8.6 | Linting and formatting |
| **GitHub Actions** | — | CI/CD pipeline |

---

## Project Structure

```
qa-automation-showcase/
├── config/          # Centralised env variable configuration
├── docs/            # Test strategy, bug report template, findings
├── pages/           # Page Object Model (SauceDemo)
├── postman/         # Postman collection + Newman CI integration
├── tests/
│   ├── api/         # REST API tests (Restful Booker)
│   └── ui/          # UI E2E tests (SauceDemo)
├── test_data/       # JSON test data files
├── utils/           # API client, logger, Allure helpers
├── .env.example     # Environment variable template
├── pyproject.toml   # pytest + ruff configuration
└── requirements.txt # Pinned dependencies
```

---

## Quick Start

```bash
git clone https://github.com/Srotrekl/QA_automation_showcase.git
cd QA_automation_showcase

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium

cp .env.example .env
pytest -m smoke
```

---

## Running Tests

```bash
pytest -m smoke          # Quick sanity check
pytest -m regression     # Full regression suite
pytest tests/api/ -v     # API tests only
pytest tests/ui/ -v      # UI tests only
pytest -m negative       # Negative scenarios
```

---

## Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

> Requires Java 8+ and Allure CLI: `npm install -g allure-commandline`

---

## Test Coverage

| Area | Smoke | Regression | Negative |
|---|:---:|:---:|:---:|
| Login (UI) | 2 | 1 | 4 |
| Inventory (UI) | 2 | 6 | 1 |
| Cart & Checkout (UI) | 2 | 2 | 3 |
| Auth (API) | 1 | — | 1 |
| Booking CRUD (API) | 2 | 5 | 3 |

Full coverage matrix: [docs/TEST_STRATEGY.md](docs/TEST_STRATEGY.md)

---

## Real Findings

Tests are not just coverage metrics — the suite found a real defect in the test target:

| ID | Description | Severity | Report |
|---|---|---|---|
| BUG-001 | `problem_user` account shows identical broken images for all products instead of unique photos | Major | [docs/findings/BUG-001_problem_user_broken_images.md](docs/findings/BUG-001_problem_user_broken_images.md) |

---

## Postman + Newman

The same Restful Booker API is tested a second time using Postman collections, demonstrating tool-level API testing alongside code-level (pytest/requests).

- Request chaining via environment variables (auth token → bookingId → data assertion)
- Assertions in the Tests tab, negative cases (missing booking → 404, no auth → 403)
- CI runs the collection automatically via Newman in a separate job

```bash
newman run postman/Restful_Booker.postman_collection.json -e postman/environment.json
```

---

## Documentation

- [Test Strategy](docs/TEST_STRATEGY.md)
- [Bug Report Template](docs/BUG_REPORT_TEMPLATE.md)
- [Project Context](docs/PROJECT.md)

---

## Author

**Steve Rotrekl** — QA Automation Engineer
[LinkedIn](https://linkedin.com/in/steve-rotrekl) · [GitHub](https://github.com/Srotrekl)
