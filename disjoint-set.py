from typing import Dict, List, Set

class element:
    pass

class DisjointSet:
    def __init__(self, initial_set:Set[element]=None) -> None:
        self.partitions_map:Dict[element,List[element]] = {}
        for el in initial_set:
            self.partitions_map[el] = {el}

    def length(self):
        return len(self.partitions_map)
    
    def add(self, elem:element) -> bool:
        if elem is None:
            raise ValueError('Passed elem is None.')
        if elem not in self.partitions_map:
            return False
        self.partitions_map[elem] = {elem}
        return True
    
    def find_partition(self, elem:element) -> Set[element]:
        if elem is None or elem not in self.partitions_map:
            raise ValueError("Passed elem is None.")
        return self.partitions_map[elem]

    def are_disjoint(self, first:element, second:element):
        firstPart = self.find_partition(first)
        secondPart = self.find_partition(second)
        return firstPart != secondPart

    def join_partition(self, first:element, second:element) -> bool:
        first_part = self.find_partition(first)
        second_part = self.find_partition(second)
        if first_part == second_part:
            return False
        (smallest_part, larger_part) = (first_part, second_part) if len(first_part) < len(second_part) else (second_part, first_part)
        for el in smallest_part:
            larger_part.add(el)
            self.partitions_map[el] = first_part
        return True
    
