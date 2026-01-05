from __future__ import annotations
from threading import Lock
from typing import Any


class SingletonMeta(type):
    _instances: dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.env = "dev"
        self.debug = True

    def set_env(self, env: str) -> None:
        self.env = env
        self.debug = (env != "prod")
