from dataclasses import dataclass, field
from typing import List
from .order_status import OrderStatus
from .order_line import OrderLine
from .money import Money
from .errors import EmptyOrderError, OrderAlreadyPaidError, OrderLockedError


@dataclass
class Order:
    id: str
    currency: str = "USD"
    status: OrderStatus = OrderStatus.DRAFT
    _lines: List[OrderLine] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            raise ValueError("Order id is required")
        if not self.currency:
            raise ValueError("Order currency is required")

    @property
    def lines(self) -> List[OrderLine]:
       
        return list(self._lines)

    def add_line(self, line: OrderLine) -> None:
        if self.status == OrderStatus.PAID:
            raise OrderLockedError("Cannot modify paid order")
        if line.unit_price.currency != self.currency:
            raise ValueError("Line currency must match order currency")
        self._lines.append(line)

    def total(self) -> Money:
        total = Money(0, self.currency)
        for line in self._lines:
            total = total + line.line_total
        return total

    def pay(self) -> Money:
        # Инварианты
        if not self._lines:
            raise EmptyOrderError("Cannot pay empty order")
        if self.status == OrderStatus.PAID:
            raise OrderAlreadyPaidError("Order already paid")

        amount = self.total()
        # переводим в PAID только после успешного чарджа в use-case,
        # но доменная операция может быть такой:
        self.status = OrderStatus.PAID
        return amount
