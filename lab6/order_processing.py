from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_CURRENCY = "USD"
TAX_RATE = 0.21

COUPON_SAVE10 = "SAVE10"
COUPON_SAVE20 = "SAVE20"
COUPON_VIP = "VIP"

SAVE10_RATE = 0.10

SAVE20_THRESHOLD = 200
SAVE20_HIGH_RATE = 0.20
SAVE20_LOW_RATE = 0.05

VIP_DISCOUNT_DEFAULT = 50
VIP_DISCOUNT_LOW_SUBTOTAL = 10
VIP_LOW_SUBTOTAL_THRESHOLD = 100

ORDER_ID_SUFFIX = "X"


@dataclass(frozen=True)
class CheckoutRequest:
    user_id: Any
    items: Any
    coupon: Any
    currency: Any


def parse_request(request: dict) -> Tuple[Any, Any, Any, Any]:
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency")
    return user_id, items, coupon, currency


def _parse_request_model(request: Dict[str, Any]) -> CheckoutRequest:
    user_id, items, coupon, currency = parse_request(request)
    return CheckoutRequest(user_id=user_id, items=items, coupon=coupon, currency=currency)


def _validate_user_id(user_id: Any) -> None:
    if user_id is None:
        raise ValueError("user_id is required")


def _validate_items(items: Any) -> List[Dict[str, Any]]:
    if items is None:
        raise ValueError("items is required")
    if type(items) is not list:
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")

    for it in items:
        if "price" not in it or "qty" not in it:
            raise ValueError("item must have price and qty")
        if it["price"] <= 0:
            raise ValueError("price must be positive")
        if it["qty"] <= 0:
            raise ValueError("qty must be positive")

    return items


def _normalize_currency(currency: Any) -> str:
    if currency is None:
        return DEFAULT_CURRENCY
    return currency


def _calculate_subtotal(items: List[Dict[str, Any]]) -> int:
    subtotal = 0
    for it in items:
        subtotal = subtotal + it["price"] * it["qty"]
    return subtotal


def _calculate_discount(subtotal: int, coupon: Any) -> int:
    if coupon is None or coupon == "":
        return 0

    if coupon == COUPON_SAVE10:
        return int(subtotal * SAVE10_RATE)

    if coupon == COUPON_SAVE20:
        if subtotal >= SAVE20_THRESHOLD:
            return int(subtotal * SAVE20_HIGH_RATE)
        return int(subtotal * SAVE20_LOW_RATE)

    if coupon == COUPON_VIP:
        discount = VIP_DISCOUNT_DEFAULT
        if subtotal < VIP_LOW_SUBTOTAL_THRESHOLD:
            discount = VIP_DISCOUNT_LOW_SUBTOTAL
        return discount

    raise ValueError("unknown coupon")


def _apply_discount(subtotal: int, discount: int) -> int:
    total_after_discount = subtotal - discount
    if total_after_discount < 0:
        total_after_discount = 0
    return total_after_discount


def _calculate_tax(amount: int) -> int:
    return int(amount * TAX_RATE)


def _build_order_id(user_id: Any, items_count: int) -> str:
    return str(user_id) + "-" + str(items_count) + "-" + ORDER_ID_SUFFIX


def process_checkout(request: dict) -> dict:
    req = _parse_request_model(request)

    _validate_user_id(req.user_id)
    items = _validate_items(req.items)
    currency = _normalize_currency(req.currency)

    subtotal = _calculate_subtotal(items)
    discount = _calculate_discount(subtotal, req.coupon)
    total_after_discount = _apply_discount(subtotal, discount)

    tax = _calculate_tax(total_after_discount)
    total = total_after_discount + tax

    order_id = _build_order_id(req.user_id, len(items))

    return {
        "order_id": order_id,
        "user_id": req.user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }