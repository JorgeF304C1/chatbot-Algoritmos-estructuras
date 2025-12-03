from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class FileSystemNode:
    name: str
    type: str  # "directory" | "file"
    children: List["FileSystemNode"] = field(default_factory=list)

    def is_directory(self) -> bool:
        return self.type == "directory"

    def find_child(self, name: str) -> Optional["FileSystemNode"]:
        for child in self.children:
            if child.name.lower() == name.lower():
                return child
        return None

    def to_dict(self) -> Dict:
        data = {"name": self.name, "type": self.type}
        if self.is_directory():
            data["children"] = [child.to_dict() for child in self.children]
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "FileSystemNode":
        children = [cls.from_dict(child) for child in data.get("children", [])]
        return cls(name=data["name"], type=data["type"], children=children)


class VirtualFileSystem:
    """In-memory tree with validation helpers."""

    def __init__(self, root: FileSystemNode):
        if not root.is_directory():
            raise ValueError("La raíz debe ser una carpeta")
        self._root = root

    @classmethod
    def from_seed(cls, data: Dict) -> "VirtualFileSystem":
        root_data = data.get("root")
        if not root_data:
            raise ValueError("Seed inválida: falta 'root'")
        return cls(FileSystemNode.from_dict(root_data))

    def list_directory(self, path: str) -> Dict[str, List[str]]:
        node = self._resolve(path)
        if not node.is_directory():
            raise ValueError(f"La ruta {path} no es una carpeta")
        folders = [child.name for child in node.children if child.is_directory()]
        files = [child.name for child in node.children if not child.is_directory()]
        return {"folders": sorted(folders), "files": sorted(files)}

    def remove_directory(self, path: str) -> str:
        if path.strip() in ("", "/"):
            raise ValueError("No se puede eliminar la raíz")
        parent, node = self._resolve_with_parent(path)
        if not node.is_directory():
            raise ValueError("Solo se pueden eliminar carpetas")
        parent.children = [child for child in parent.children if child is not node]
        return node.name

    def make_directory(self, path: str) -> str:
        normalized = path.strip()
        if normalized in ("", "/"):
            raise ValueError("Debe indicar la ruta completa de la nueva carpeta")
        parts = self._split(normalized)
        if len(parts) < 2:
            raise ValueError("La ruta debe incluir la carpeta raíz y el nombre a crear")
        new_name = parts[-1]
        parent_path = "/" + "/".join(parts[:-1])
        parent = self._resolve(parent_path)
        if not parent.is_directory():
            raise ValueError("Solo se pueden crear carpetas dentro de otras carpetas")
        if parent.find_child(new_name):
            raise ValueError(f"Ya existe '{new_name}' en la ruta indicada")
        parent.children.append(FileSystemNode(name=new_name, type="directory"))
        return new_name

    def snapshot(self) -> Dict:
        return {"root": self._root.to_dict()}

    @property
    def root_name(self) -> str:
        return self._root.name

    def _resolve(self, path: str) -> FileSystemNode:
        parent, node = self._resolve_with_parent(path)
        return node

    def _resolve_with_parent(self, path: str) -> (FileSystemNode, FileSystemNode):
        normalized = path.strip()
        parts = self._split(normalized)
        if not parts:
            return self._root, self._root
        node = self._root
        parent = self._root
        if parts[0].lower() != self._root.name.lower():
            raise ValueError(f"La ruta debe iniciar en /{self._root.name}")
        for idx, part in enumerate(parts[1:], start=1):
            parent = node
            next_node = node.find_child(part)
            if not next_node:
                raise ValueError(f"Ruta inválida: {'/'.join(parts[:idx + 1])}")
            node = next_node
        return parent, node

    @staticmethod
    def _split(path: str) -> List[str]:
        if not path or path == "/":
            return []
        cleaned = path.strip("/")
        return [segment for segment in cleaned.split("/") if segment]
