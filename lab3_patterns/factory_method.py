from __future__ import annotations
from abc import ABC, abstractmethod


class Transport(ABC):
    @abstractmethod
    def deliver(self, payload: str) -> str:
        raise NotImplementedError


class Truck(Transport):
    def deliver(self, payload: str) -> str:
        return f"Truck delivers '{payload}' by road."


class Ship(Transport):
    def deliver(self, payload: str) -> str:
        return f"Ship delivers '{payload}' by sea."


class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:
        raise NotImplementedError

    def plan_delivery(self, payload: str) -> str:
        return self.create_transport().deliver(payload)


class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()
