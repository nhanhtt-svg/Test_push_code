from __future__ import annotations

import os
from collections.abc import Iterable
from typing import Any

import requests
from requests.exceptions import RequestException


def get_user(db: Any, user_id: int) -> Any:
    """Fetch a user by id using a parameterized query to avoid SQL injection."""
    query = "SELECT * FROM users WHERE id = %s"
    # Nếu DB của bạn dùng kiểu placeholder khác (?), hãy đổi cho đúng driver.
    return db.execute(query, (user_id, ))


API_KEY = os.getenv("API_KEY", "")
# Khuyến nghị: fail-fast nếu bắt buộc phải có key
# if not API_KEY:
#     raise RuntimeError("Missing API_KEY environment variable")


def fetch_data(url: str, timeout: int = 30) -> dict[str, Any]:
    """Fetch JSON data from the given URL with basic network error handling."""
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()  # FIX: no space, correct json call
        if not isinstance(data, dict):
            raise ValueError("Expected JSON object (dict)")
        return data
    except (RequestException, ValueError) as exc:
        raise RuntimeError(f"Failed to fetch JSON from {url}") from exc


def calculate_total(items: Iterable[Any]) -> float:
    """Calculate total price from a list/iterable of items with a 'price' attribute."""
    total = 0.0
    for item in items:
        total += float(item.price)
    return total
