# QA Automation Showcase

![CI](https://github.com/<username>/qa-automation-showcase/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

End-to-end UI a REST API test suite nad **SauceDemo** a **Restful Booker** — pytest, Playwright, requests, Allure reporting.

## Tech Stack

| Technologie | Verze | Účel |
|-------------|-------|------|
| **pytest** | 8.3.4 | Test runner, fixtures, markery |
| **Playwright** | 1.49.1 | UI E2E testy (POM) |
| **requests** | 2.32.3 | REST API testy |
| **Allure** | 2.13.5 | Reporting (kroky, screenshoty) |
| **pydantic-settings** | 2.7.1 | Konfigurace (env variables) |
| **jsonschema** | 4.23.0 | API response validace |
| **ruff** | 0.8.6 | Linting + formátování |
| **GitHub Actions** | — | CI/CD pipeline |

## Architektura

```
qa-automation-showcase/
├── config/          # Centrální konfigurace (env variables)
├── docs/            # Test strategy, bug report template
├── pages/           # Page Object Model (SauceDemo)
├── tests/
│   ├── api/         # REST API testy (Restful Booker)
│   └── ui/          # UI E2E testy (SauceDemo)
├── test_data/       # Testovací data (JSON)
├── utils/           # API client, logger, Allure helpers
├── .env.example     # Ukázkový .env
├── pyproject.toml   # pytest + ruff konfigurace
└── requirements.txt # Pinned závislosti
```

## Quick Start

```bash
# 1. Klonuj repozitář
git clone https://github.com/<username>/qa-automation-showcase.git
cd qa-automation-showcase

# 2. Vytvoř a aktivuj virtuální prostředí
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Nainstaluj závislosti
pip install -r requirements.txt

# 4. Nainstaluj Playwright prohlížeče
playwright install chromium

# 5. Nastav environment variables
cp .env.example .env
# Uprav .env pokud potřebuješ změnit výchozí hodnoty

# 6. Spusť smoke testy
pytest -m smoke
```

## Spouštění testů

```bash
# Smoke testy (rychlá kontrola)
pytest -m smoke

# Kompletní regrese
pytest -m regression

# Jen API testy
pytest tests/api/ -v

# Jen UI testy
pytest tests/ui/ -v

# Negative testy
pytest -m negative

# Konkrétní soubor
pytest tests/ui/test_login.py -v
```

## Allure Report

```bash
# Spusť testy s Allure výstupem
pytest --alluredir=allure-results

# Otevři report v prohlížeči
allure serve allure-results
```

> **Prerequisite:** Allure CLI vyžaduje Java Runtime (JRE 8+).
> Instalace: `npm install -g allure-commandline` nebo [allure docs](https://docs.qameta.io/allure/).

## Testovací pokrytí

Detailní matice pokrytí viz [docs/TEST_STRATEGY.md](docs/TEST_STRATEGY.md).

| Oblast | Smoke | Regression | Negative |
|--------|:-----:|:----------:|:--------:|
| Login (UI) | 2 | 1 | 2 |
| Inventory (UI) | 2 | 5 | — |
| Cart & Checkout (UI) | 2 | 2 | 2 |
| Auth (API) | 1 | — | 1 |
| Booking CRUD (API) | 2 | 5 | 3 |

## Prerequisites

- **Python** 3.11+
- **Java** 8+ (pro Allure CLI)
- **Node.js** (volitelné, pro `npm install -g allure-commandline`)
- **OS:** Windows, Linux, macOS

## Dokumentace

- [Test Strategy](docs/TEST_STRATEGY.md) — scope, typy testů, matice pokrytí
- [Bug Report Template](docs/BUG_REPORT_TEMPLATE.md) — šablona pro reportování
- [O projektu](docs/PROJECT.md) — kontext, motivace, co bych přidal v produkci

## Autor

**Steve** — QA Automation Engineer
<!-- LinkedIn: https://linkedin.com/in/xxx -->
