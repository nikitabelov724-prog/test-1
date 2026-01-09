from enum import Enum


class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    PAID = "PAID"
