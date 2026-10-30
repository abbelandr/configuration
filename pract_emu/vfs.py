import base64
import json
import os


class VFSNode:
    def __init__(self, name, is_dir=True, content=""):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children = {} if is_dir else None


class VFS:
    def __init__(self):
        self.root = VFSNode("/")
        self.cwd = self.root

    def load_from_json(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"VFS file not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self._build_tree(self.root, data)

    def _build_tree(self, current_node, data):
        # Рекурсивное построение дерева из JSON
        for child_data in data.get("children", []):
            name = child_data["name"]
            node_type = child_data["type"]
            is_dir = (node_type == "dir")

            content = ""
            if not is_dir:
                b64_content = child_data.get("content", "")
                try:
                    content = base64.b64decode(b64_content).decode('utf-8')
                except Exception:
                    content = b64_content  # Если не Base64, оставляем как есть

            new_node = VFSNode(name, is_dir, content)
            current_node.children[name] = new_node

            if is_dir:
                self._build_tree(new_node, child_data)

    def resolve_path(self, path, must_exist=True):
        if not path or path == ".": return self.cwd
        if path == "/": return self.root

        current = self.root if path.startswith("/") else self.cwd
        parts = [p for p in path.split("/") if p]

        for part in parts:
            if part == "..":
                if current.name != "/":
                    current = self._find_parent(current) or self.root
            else:
                if current.is_dir and part in current.children:
                    current = current.children[part]
                else:
                    if must_exist: raise FileNotFoundError(f"Нет такого файла или каталога: {path}")
                    return None
        return current

    def _find_parent(self, target_node):
        def dfs(node):
            if not node.is_dir: return None
            for child in node.children.values():
                if child == target_node: return node
                res = dfs(child)
                if res: return res
            return None

        return dfs(self.root)

    def get_prompt_path(self):
        parts = []
        curr = self.cwd
        while curr and curr.name != "/":
            parts.append(curr.name)
            curr = self._find_parent(curr)
        return "/" + "/".join(reversed(parts)) if parts else "/"

    def list_dir(self, path=None):
        node = self.resolve_path(path) if path else self.cwd
        if not node.is_dir: raise NotADirectoryError(f"Не каталог: {path}")
        return list(node.children.values()) if node.children else []

    def change_dir(self, path):
        node = self.resolve_path(path)
        if not node.is_dir: raise NotADirectoryError(f"Не каталог: {path}")
        self.cwd = node

    def read_file(self, path):
        node = self.resolve_path(path)
        if node.is_dir: raise IsADirectoryError(f"Это каталог: {path}")
        return node.content

    def mkdir(self, path):
        parent_path = os.path.dirname(path) or "."
        dir_name = os.path.basename(path)
        parent = self.resolve_path(parent_path)
        if not parent.is_dir: raise NotADirectoryError(f"Не каталог: {parent_path}")
        if dir_name in parent.children: raise FileExistsError(f"Файл существует: {path}")
        parent.children[dir_name] = VFSNode(dir_name, is_dir=True)

    def touch(self, path):
        parent_path = os.path.dirname(path) or "."
        file_name = os.path.basename(path)
        parent = self.resolve_path(parent_path)
        if not parent.is_dir: raise NotADirectoryError(f"Не каталог: {parent_path}")
        if file_name not in parent.children:
            parent.children[file_name] = VFSNode(file_name, is_dir=False, content="")