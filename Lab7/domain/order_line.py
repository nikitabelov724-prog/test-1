from dataclasses import dataclass
from .money import Money


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    unit_price: Money
    quantity: int

    def __post_init__(self):
        if not self.product_id:
            raise ValueError("product_id is required")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")

    @property
    def line_total(self) -> Money:
        return Money(self.unit_price.amount * self.quantity, self.unit_price.currency)
