"""Helper funkce pro Allure reporting.

Standardizované attachmenty — response body, screenshoty, JSON data.
"""

from typing import Any

import allure


def attach_response(response: Any, name: str = "API Response") -> None:
    """Attachne HTTP response body do Allure reportu.

    Args:
        response: requests.Response objekt.
        name: Název attachmentu v reportu.
    """
    try:
        body = response.json()
    except (ValueError, AttributeError):
        body = str(response)

    allure.attach(
        str(body),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_json(data: dict[str, Any] | list[Any], name: str = "JSON Data") -> None:
    """Attachne libovolná JSON data do Allure reportu."""
    import json

    allure.attach(
        json.dumps(data, indent=2, ensure_ascii=False),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )
