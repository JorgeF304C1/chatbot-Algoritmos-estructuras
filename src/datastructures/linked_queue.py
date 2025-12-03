from __future__ import annotations

from typing import Generic, Iterable, Iterator, Optional, TypeVar

from .nodes import Node

T = TypeVar("T")


class LinkedQueue(Generic[T]):
    """Queue implemented with singly linked nodes."""

    def __init__(self, values: Optional[Iterable[T]] = None):
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._size = 0
        if values:
            for value in values:
                self.enqueue(value)

    def enqueue(self, value: T) -> None:
        node = Node(value)
        if not self._head:
            self._head = self._tail = node
        else:
            assert self._tail is not None
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self) -> T:
        if not self._head:
            raise IndexError("La cola está vacía")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value  # type: ignore[return-value]

    def peek(self) -> T:
        if not self._head:
            raise IndexError("La cola está vacía")
        return self._head.value  # type: ignore[return-value]

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current:
            yield current.value  # type: ignore[misc]
            current = current.next
