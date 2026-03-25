# O projektu

## Účel

Demonstrace QA automation skillů na reálných veřejných aplikacích.
Portfolio projekt pro pozice Software QA Engineer / Test Automation Engineer.

## Co tento projekt ukazuje

- **Test automatizace na UI i API úrovni** — Playwright pro E2E, requests pro REST API
- **Testovací architektura** — Page Object Model, oddělení vrstev (tests/pages/utils/config)
- **CI/CD integrace** — GitHub Actions s matrix strategií a Allure reportingem
- **Čistý kód** — type hints, docstringy, konzistentní konvence, žádná duplicita
- **Bezpečnost** — secrets management (.env, GitHub Secrets), pre-commit hooks
- **QA principy** — smoke/regression/negative testy, test strategy, bug report template

## Testované aplikace

| Aplikace | Proč jsem ji vybral |
|----------|-------------------|
| **SauceDemo** | Standardní demo e-shop pro QA — kompletní flow (login → inventory → cart → checkout), záměrně buggy uživatelé pro negative testy, veřejné credentials |
| **Restful Booker** | Realistické REST API s CRUD operacemi a token-based auth — víc "production-like" než jednodušší alternativy (Reqres.in) |

## Jak projekt vznikal

Projekt byl budovaný postupně v 6 fázích, kde každá fáze odpovídá jednomu PR:

1. **Project scaffold** — konfigurace, dependencies, dokumentace
2. **POM + UI smoke testy** — Page Object Model, první Playwright testy
3. **API testy** — requests wrapper, CRUD testy, JSON validace
4. **Rozšířené UI testy** — parametrizace, cross-browser, checkout flow
5. **Negative testy + CI/CD** — error handling, GitHub Actions pipeline
6. **Finalizace** — README, test strategy, code review

## Co bych přidal v reálném projektu

- **Docker** — kontejnerizovaný test runner pro konzistentní prostředí
- **Vlastní test data management** — databáze/API pro generování a cleanup test dat
- **Paralelizace** — pytest-xdist pro rychlejší běh na CI
- **Integrace s Jirou** — automatické vytváření ticketů z failujících testů
- **Visual regression** — screenshot porovnání (Playwright snapshots)
- **API contract testing** — Pact nebo similar pro ověření API kontraktů
- **Monitoring** — Grafana dashboard s historickými test výsledky
