from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class RequestType(Enum):
    TYPE_A = auto()
    TYPE_B = auto()
    TYPE_C = auto()


@dataclass(frozen=True)
class Request:
    type: RequestType
    payload: str = ""


class Handler:
    def __init__(self) -> None:
        self._next: Optional["Handler"] = None

    def set_next(self, nxt: "Handler") -> "Handler":
        self._next = nxt
        return nxt

    def handle(self, request: Request) -> str:
        if self._next:
            return self._next.handle(request)
        return f"No handler for {request.type.name}"


class ConcreteHandlerA(Handler):
    def handle(self, request: Request) -> str:
        if request.type == RequestType.TYPE_A:
            return f"HandlerA processed: {request.payload}"
        return super().handle(request)


class ConcreteHandlerB(Handler):
    def handle(self, request: Request) -> str:
        if request.type == RequestType.TYPE_B:
            return f"HandlerB processed: {request.payload}"
        return super().handle(request)


class ConcreteHandlerC(Handler):
    def handle(self, request: Request) -> str:
        if request.type == RequestType.TYPE_C:
            return f"HandlerC processed: {request.payload}"
        return super().handle(request)
