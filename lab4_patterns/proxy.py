from __future__ import annotations
from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def query(self, sql: str) -> str:
        raise NotImplementedError


class RealDatabase(Database):
    def query(self, sql: str) -> str:
        # тут могла бы быть настоящая работа с БД
        return f"Executing query: {sql}"


class DatabaseProxy(Database):
    def __init__(self, has_access: bool) -> None:
        self._has_access = has_access
        self._real: RealDatabase | None = None  # lazy init

    def query(self, sql: str) -> str:
        if not self._has_access:
            return "Access denied. Query cannot be executed."
        if self._real is None:
            self._real = RealDatabase()
        return self._real.query(sql)
