from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, arr: List[int]) -> List[int]:
        raise NotImplementedError


class BubbleSortStrategy(SortingStrategy):
    def sort(self, arr: List[int]) -> List[int]:
        a = list(arr)
        n = len(a)
        for i in range(n):
            for j in range(0, n - i - 1):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
        return a


class QuickSortStrategy(SortingStrategy):
    def sort(self, arr: List[int]) -> List[int]:
        a = list(arr)
        if len(a) <= 1:
            return a
        pivot = a[len(a) // 2]
        left = [x for x in a if x < pivot]
        mid = [x for x in a if x == pivot]
        right = [x for x in a if x > pivot]
        return self.sort(left) + mid + self.sort(right)


@dataclass
class Sorter:
    strategy: SortingStrategy

    def set_strategy(self, strategy: SortingStrategy) -> None:
        self.strategy = strategy

    def sort_array(self, arr: List[int]) -> List[int]:
        return self.strategy.sort(arr)
