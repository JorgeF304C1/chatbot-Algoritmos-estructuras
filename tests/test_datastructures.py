import json
from pathlib import Path

import pytest

from src.datastructures.linked_queue import LinkedQueue
from src.datastructures.linked_stack import LinkedStack
from src.services.virtual_fs import VirtualFileSystem


def test_linked_stack_basic_operations():
    stack = LinkedStack()
    stack.push("a")
    stack.push("b")
    assert len(stack) == 2
    assert stack.pop() == "b"
    assert stack.pop() == "a"


def test_linked_queue_basic_operations():
    queue = LinkedQueue()
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.dequeue() == 1
    assert queue.dequeue() == 2


def test_virtual_filesystem_removal(tmp_path):
    seed_path = Path(__file__).resolve().parents[1] / "data" / "default_fs.json"
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    fs = VirtualFileSystem.from_seed(seed)
    listing = fs.list_directory(f"/{fs.root_name}")
    assert "Fotos" in listing["folders"]
    fs.remove_directory(f"/{fs.root_name}/Fotos")
    listing_after = fs.list_directory(f"/{fs.root_name}")
    assert "Fotos" not in listing_after["folders"]


def test_virtual_filesystem_creation(tmp_path):
    seed_path = Path(__file__).resolve().parents[1] / "data" / "default_fs.json"
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    fs = VirtualFileSystem.from_seed(seed)
    fs.make_directory(f"/{fs.root_name}/Nueva")
    listing = fs.list_directory(f"/{fs.root_name}")
    assert "Nueva" in listing["folders"]
    with pytest.raises(ValueError):
        fs.make_directory(f"/{fs.root_name}/Nueva")
