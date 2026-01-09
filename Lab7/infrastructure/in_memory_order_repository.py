from domain.order import Order
from application.ports import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._storage: dict[str, Order] = {}

    def add(self, order: Order) -> None:
        self._storage[order.id] = order

    def get_by_id(self, order_id: str) -> Order:
        if order_id not in self._storage:
            raise KeyError(f"Order not found: {order_id}")
        return self._storage[order_id]

    def save(self, order: Order) -> None:
        self._storage[order.id] = order
