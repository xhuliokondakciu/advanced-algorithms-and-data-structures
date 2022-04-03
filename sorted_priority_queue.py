from __future__ import annotations


class Node:
    def __init__(self, key: any, priority: float) -> None:
        self.key = key
        self.priority = priority
        self.left: Node = None
        self.right: Node = None
        self.parent: Node = None

    def set_left(self, node: Node) -> None:
        self.left = node
        if node is not None:
            node.parent = self

    def set_right(self, node: Node) -> None:
        self.right = node
        if node is not None:
            node.parent = self


class Treap:
    def __init__(self) -> None:
        self.root: Node = None

    def _is_root(self, node: Node) -> bool:
        return node == self.root

    def _is_empty(self) -> bool:
        return self.root is None

    def _is_leaf(self, node: Node) -> bool:
        return node.left is None and node.right is None

    def _rotate(self, node: Node) -> None:
        if node is None or self._is_root(node):
            raise ValueError("Node cannot be none or root.")

        if node.parent is None:
            return

        left_rotate: bool = False
        if node.parent.right == node:
            left_rotate = True

        node_parent = node.parent
        if (
            node_parent.left != node
            and not left_rotate
            or node_parent.right != node
            and left_rotate
        ):
            raise ValueError("Given node is not in the correct side.")
        ultimate_parent = node_parent.parent

        if ultimate_parent is not None:
            if ultimate_parent.left is node_parent:
                ultimate_parent.set_left(node)
            else:
                ultimate_parent.set_right(node)
        else:
            self.root = node
        if left_rotate:
            node_parent.set_right(node.left)
            node.set_left(node_parent)
        else:
            node_parent.set_left(node.right)
            node.set_right(node_parent)
        
        node.parent = ultimate_parent

    def top(self) -> bool:
        if self._is_empty():
            raise ValueError("Treap is empty")
        to_remove = self.root.key
        self.remove(to_remove)
        return to_remove

    def peek(self):
        if self.root is None:
            raise ValueError("Treap is emtpy.")
        return self.root

    def insert(self, key, priority) -> Node:
        new_node = Node(key, priority)
        if self._is_empty():
            self.root = new_node
            return

        current_node = parent_node = self.root
        while current_node is not None:
            parent_node = current_node
            if key > current_node.key:
                current_node = current_node.right
            else:
                current_node = current_node.left

        # Out of loop, we found the parent where to insert
        if key > parent_node.key:
            parent_node.right = new_node
        else:
            parent_node.left = new_node
        new_node.parent = parent_node

        while (
            new_node.parent is not None and new_node.priority < new_node.parent.priority
        ):
            self._rotate(new_node)

    def remove(self, key) -> bool:
        node = self.search(key)
        if node is None:
            return False
        if self._is_root(node) and self._is_leaf(node):
            self.root = None
            return False

        while not self._is_leaf(node):
            if node.left is not None and (
                node.right is None or node.left.priority > node.right.priority
            ):
                self._rotate(node.right)
            else:
                self._rotate(node.left)

            if self._is_root(node):
                self.root = node.left

        if node.parent.left == node:
            node.parent.left = None
        else:
            node.parent.right = None

        return True

    def update(self, key, new_priority) -> bool:
        if self._is_empty():
            raise ValueError("Treap is empty.")

        node = self.search(key)
        if node is None:
            return False

        node.priority = new_priority
        if self._is_root(node) and self._is_leaf(node):
            return True

        while (
            (
                self_rotate := (
                    node.parent is not None and node.priority < node.parent.priority
                )
            )
            or (
                left_node_rotate := (
                    node.left is not None and node.priority > node.left.priority
                )
            )
            or (node.right is not None and node.priority > node.right.priority)
        ):
            if self_rotate:
                self._rotate(node)
            elif left_node_rotate:
                self._rotate(node.left)
            else:
                self._rotate(node.right)

    def contains(self, key: any) -> bool:
        return self.search(key) is not None

    def min(self) -> any:
        if self._is_empty():
            raise ValueError("Treap is empty.")

        current_min = self.root
        while current_min.left is not None:
            current_min = current_min.left

        return current_min.key

    def max(self) -> any:
        if self._is_empty():
            raise ValueError("Treap is empty.")

        current_max: Node = self.root
        while current_max.right is not None:
            current_max = current_max.right

        return current_max.key

    def search(self, target_key) -> any:
        current_node: Node = self.root
        while current_node is not None and current_node.key != target_key:
            if target_key > current_node.key:
                current_node = current_node.right
            else:
                current_node = current_node.left

        return None if current_node is None else current_node.key
    
    def max_height(self):
        return self.max_height_inner(self.root)

    def max_height_inner(self, node:Node) -> int:
        if node is None:
            return 0

        left_height = self.max_height_inner(node.left)
        right_height = self.max_height_inner(node.right)

        return 1 + max(left_height, right_height)
