from __future__ import annotations
from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def print(self, data: str) -> str:
        raise NotImplementedError


class Monitor(Device):
    def print(self, data: str) -> str:
        return f"Displaying on monitor: {data}"


class Printer(Device):
    def print(self, data: str) -> str:
        return f"Printing to paper: {data}"


class Output(ABC):
    def __init__(self, device: Device) -> None:
        self._device = device

    @abstractmethod
    def render(self, data: str) -> str:
        raise NotImplementedError


class TextOutput(Output):
    def render(self, data: str) -> str:
        return self._device.print(f"Text: {data}")


class ImageOutput(Output):
    def render(self, data: str) -> str:
        return self._device.print(f"Image: [Binary data: {data}]")
