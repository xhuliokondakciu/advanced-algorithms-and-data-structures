from os import remove
from typing import List, Dict

class TrieNode:
    def __init__(self) -> None:
        self.key_node:bool = False
        self.children:Dict[str,TrieNode] = {}

class StringContainer:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, key:str):
        if not key:
            return False

        current_node = self.root
        for c in key:
            if c in current_node.children:
                current_node = current_node.children[c]
            else:
                new_node = TrieNode()
                current_node.children[c] = new_node
                current_node = new_node
        if not current_node.key_node:
            current_node.key_node = True

    def remove(self, key:str) -> bool:
        deleted = self._remove(self.root, key)[0]
        return deleted

    def _remove(self, node:TrieNode, key:str):
        if not key:
            deleted = node.key_node
            node.key_node = False
            should_prune = len(node.children) == 0
            return (deleted, should_prune)
        
        current_char = key[0]
        new_key = key[1:]
        if current_char in node.children:
            deleted, should_prune = self._remove(node.children[current_char], new_key)
            if deleted and should_prune:
                del node.children[current_char]
                if node.key_node or len(node.children) > 0:
                    should_prune = False
            return deleted, should_prune

        return False, False

    def contains(self, key:str) -> bool:
        if not key:
            return False

        found_node = self._find_node(self.root, key)
        return True if found_node and found_node.key_node else False

    def _find_node(self, node:TrieNode, key:str) ->TrieNode:
        if not key or not node:
            return None

        current_node = node
        for c in key:
            if c in current_node.children:
                current_node = current_node.children[c]
            else:
                return None
        
        return current_node

    def longest_prefix(self, key:str) -> int:
        pass

    def keys_starting_with(self, prefix:str) -> List[str]:
        pass


dictionary = StringContainer()
dictionary.insert("ckemi")
# dictionary.remove("ckemi")
print(dictionary.contains("ckemi"))
print(dictionary.contains("ckemisijeti"))
