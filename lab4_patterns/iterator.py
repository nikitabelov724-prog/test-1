from __future__ import annotations
from typing import Generic, Iterable, Iterator as PyIterator, List, TypeVar

T = TypeVar("T")


class Iterator(Generic[T]):
    def has_next(self) -> bool:
        raise NotImplementedError

    def next(self) -> T:
        raise NotImplementedError


class ArrayIterator(Iterator[T]):
    def __init__(self, items: List[T]) -> None:
        self._items = items
        self._pos = 0

    def has_next(self) -> bool:
        return self._pos < len(self._items)

    def next(self) -> T:
        if not self.has_next():
            raise IndexError("No more items")
        item = self._items[self._pos]
        self._pos += 1
        return item


class IterableCollection(Generic[T]):
    """
    Collection that can provide our custom iterator.
    """
    def __init__(self, items: Iterable[T]) -> None:
        self._items = list(items)

    def iterator(self) -> ArrayIterator[T]:
        return ArrayIterator(self._items)

    # optional: allow python-native iteration too
    def __iter__(self) -> PyIterator[T]:
        return iter(self._items)
