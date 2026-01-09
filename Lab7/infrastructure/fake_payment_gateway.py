from application.ports import PaymentGateway
from domain.money import Money


class FakePaymentGateway(PaymentGateway):
    def __init__(self):
        self.charges: list[tuple[str, Money]] = []

    def charge(self, order_id: str, money: Money) -> str:
        self.charges.append((order_id, money))
        return f"tx_{order_id}_{len(self.charges)}"
