from __future__ import annotations
from abc import ABC, abstractmethod


class ExternalLogger:
    def log_message(self, msg: str) -> str:
        return f"External log: {msg}"


class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> str:
        raise NotImplementedError


class LoggerAdapter(Logger):
    def __init__(self, external: ExternalLogger) -> None:
        self._external = external

    def log(self, message: str) -> str:
        return self._external.log_message(message)
