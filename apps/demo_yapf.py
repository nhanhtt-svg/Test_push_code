# import os,sys   # Ruff: E401 (multiple imports), I001 (import format), F401 (unused)

# API_KEY = "AKIA1234567890ABCDEF"  # (tuỳ cấu hình gitleaks) có thể bị flag như secret pattern

# def hello(  ):
#   print("hi")  # nếu bạn bỏ no_print thì dòng này chỉ để tạo style lỗi
#   return 1

# def complex_func(x):
#   # Tạo complexity + nested blocks + loop depth >= 3
#   total=0
#   for i in range(len(x)):
#     if i % 2 == 0:
#       for j in range(3):
#         if j > 0:
#           for k in range(2):   # nested loop depth = 3 (custom nested_loops sẽ fail)
#             if k == 1:
#               total = total + i + j + k
#             else:
#               total = total + i
#         else:
#           total += j
#     else:
#       if i > 10:
#         total += i
#       else:
#         total -= i

#   # thêm vài nhánh để tăng complexity
#   if total > 100:
#     total += 1
#   elif total > 50:
#     total += 2
#   elif total > 10:
#     total += 3
#   else:
#     total += 4

#   return total


# def messy_strings(name):
#   # YAPF/Ruff: spacing, quotes, etc.
#   msg= "Hello,"+name
#   return msg


# class MyClass(  object ):
#   def __init__(self,  value ):
#     self.value=value

#   def method(self,a,b):
#     # Ruff: unused vars; formatting issues
#     unused = 123
#     if a:
#       if b:
#         if a and b:
#           return self.value
#     return None


# def import_unused():
#   # Ruff: F401 unused import inside function
#   import json
#   return "ok"


from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import re


# ===== Basic math =====
def add(a: int, b: int) -> int:
    return a + b


def safe_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("b must not be zero")
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


# ===== String utils =====
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
