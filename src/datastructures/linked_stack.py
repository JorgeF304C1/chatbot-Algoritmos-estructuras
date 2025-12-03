from __future__ import annotations

from typing import Generic, Iterable, Iterator, Optional, TypeVar

from .nodes import Node

T = TypeVar("T")


class LinkedStack(Generic[T]):
    """Stack implemented with singly linked nodes."""

    def __init__(self, values: Optional[Iterable[T]] = None):
        self._top: Optional[Node] = None
        self._size = 0
        if values:
            for value in values:
                self.push(value)

    def push(self, value: T) -> None:
        self._top = Node(value, self._top)
        self._size += 1

    def pop(self) -> T:
        if not self._top:
            raise IndexError("La pila está vacía")
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.value  # type: ignore[return-value]

    def peek(self) -> T:
        if not self._top:
            raise IndexError("La pila está vacía")
        return self._top.value  # type: ignore[return-value]

    def clear(self) -> None:
        self._top = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        current = self._top
        while current:
            yield current.value  # type: ignore[misc]
            current = current.next
