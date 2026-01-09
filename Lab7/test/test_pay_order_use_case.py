import pytest

from domain.order import Order
from domain.order_line import OrderLine
from domain.money import Money
from domain.order_status import OrderStatus
from domain.errors import EmptyOrderError, OrderAlreadyPaidError, OrderLockedError

from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway
from application.pay_order_use_case import PayOrderUseCase


def test_success_pay_correct_order():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    uc = PayOrderUseCase(repo, gateway)

    order = Order(id="1", currency="USD")
    order.add_line(OrderLine("p1", Money(1000, "USD"), 2))  # 20.00
    order.add_line(OrderLine("p2", Money(500, "USD"), 1))   # 5.00
    repo.add(order)

    res = uc.execute("1")

    assert res.status == "PAID"
    assert res.paid_amount == 2500
    assert res.currency == "USD"
    assert res.transaction_id is not None
    assert len(gateway.charges) == 1


def test_error_pay_empty_order():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    uc = PayOrderUseCase(repo, gateway)

    order = Order(id="2", currency="USD")
    repo.add(order)

    with pytest.raises(EmptyOrderError):
        uc.execute("2")


def test_error_pay_twice():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    uc = PayOrderUseCase(repo, gateway)

    order = Order(id="3", currency="USD")
    order.add_line(OrderLine("p1", Money(100, "USD"), 1))
    repo.add(order)

    uc.execute("3")
    with pytest.raises(OrderAlreadyPaidError):
        uc.execute("3")


def test_cannot_modify_after_paid():
    order = Order(id="4", currency="USD")
    order.add_line(OrderLine("p1", Money(100, "USD"), 1))
    order.pay()  # переводим в PAID

    with pytest.raises(OrderLockedError):
        order.add_line(OrderLine("p2", Money(100, "USD"), 1))


def test_total_equals_sum_of_lines():
    order = Order(id="5", currency="USD")
    order.add_line(OrderLine("p1", Money(100, "USD"), 3))  # 300
    order.add_line(OrderLine("p2", Money(250, "USD"), 2))  # 500
    assert order.total().amount == 800
