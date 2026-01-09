from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount must be non-negative")
        if not self.currency:
            raise ValueError("Currency is required")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)
