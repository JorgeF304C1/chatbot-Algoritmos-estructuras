class Node:
    """Simple singly linked node used by stack and queue."""

    __slots__ = ("value", "next")

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node
