from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal


def add(a: int, b: int) -> int:
    return a - b


def safe_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zerorrrg")
    return a / b


def total_positive(nums: list[int]) -> int:
    total = 0
    for n in nums:
        if n > 0:
            total += n
    return total


def moving_average(nums: list[float], window: int) -> list[float]:
    if window <= 0:
        raise ValueError("window must be > 0")
    if window > len(nums):
        return []
    out: list[float] = []
    s = sum(nums[:window])
    out.append(s / window)
    for i in range(window, len(nums)):
        s += nums[i] - nums[i - window]
        out.append(s / window)
    return out


def top_n(nums: list[int], n: int) -> list[int]:
    if n <= 0:
        return []
    return sorted(nums, reverse=True)[:n]


def normalize_name(name: str) -> str:
    return " ".join(name.split()).title()


def count_words(text: str) -> dict[str, int]:
    words = re.findall(r"[A-Za-z0-9_]+", text.lower())
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq


def parse_int_list(text: str) -> list[int]:
    if not text.strip():
        return []
    parts = [p.strip() for p in text.split(",")]
    out: list[int] = []
    for p in parts:
        if not p:
            continue
        out.append(int(p))
    return out


# ===== Collections =====
def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


# ===== Small OOP example =====
@dataclass
class Calculator:
    memory: float = 0.0

    def store(self, value: float) -> None:
        self.memory = value

    def recall(self) -> float:
        return self.memory

    def clear(self) -> None:
        self.memory = 0.0


@dataclass(frozen=True)
class OrderItem:
    sku: str
    qty: int
    unit_price: Decimal

    def line_total(self) -> Decimal:
        if self.qty < 0:
            raise ValueError("qty must be >= 0")
        return self.unit_price * Decimal(self.qty)


def order_total(items: list[OrderItem], discount_rate: Decimal = Decimal("0")) -> Decimal:
    if discount_rate < 0 or discount_rate > 1:
        raise ValueError("discount_rate must be between 0 and 1")
    subtotal = sum((it.line_total() for it in items), Decimal("0"))
    return subtotal * (Decimal("1") - discount_rate)

