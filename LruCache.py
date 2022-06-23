import queue
from typing import Dict, List, Set
from collections import deque

class LruCache:
    def __init__(self, max_elements:int) -> None:
        self.max_size = max_elements
        self.hash_table:set = set()
        self.elements:deque = deque()
    
    def set(self, key, value):
        if key in self.hash_table:
            
