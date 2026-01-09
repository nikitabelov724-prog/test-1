from dataclasses import dataclass
from domain.errors import DomainError
from domain.order_status import OrderStatus
from .ports import OrderRepository, PaymentGateway


@dataclass(frozen=True)
class PayOrderResult:
    order_id: str
    status: str
    transaction_id: str | None
    paid_amount: int | None
    currency: str | None


class PayOrderUseCase:
    def __init__(self, repo: OrderRepository, gateway: PaymentGateway):
        self.repo = repo
        self.gateway = gateway

    def execute(self, order_id: str) -> PayOrderResult:
        order = self.repo.get_by_id(order_id)

        # доменная операция: проверка инвариантов + (предварительное) изменение статуса
        amount = order.pay()

        # платёж во внешнем мире
        tx_id = self.gateway.charge(order.id, amount)

        # сохранить
        self.repo.save(order)

        return PayOrderResult(
            order_id=order.id,
            status=order.status.value,
            transaction_id=tx_id,
            paid_amount=amount.amount,
            currency=amount.currency,
        )
