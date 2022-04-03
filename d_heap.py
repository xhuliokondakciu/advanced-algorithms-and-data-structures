from typing import List


class EmptyHeapError(BaseException):
    pass


class DHeapItem(object):
    def __init__(self, value: str, priority: int):
        self.value = value
        self.priority = priority

    def __format__(self, format_spec):
        return f"value={self.value}, priority={self.priority}"


class DHeap:
    def __heapify(self):
        """Heapifies the current heap"""
        for index in (len(self.pairs) - 1) / 2:
            self.__push_down(index)

    def __get_parent_index(self, index):
        return (index - 1) // self.arity

    def __bubble_up(self, index: int) -> None:
        parent_index = current_index = index
        item_to_move_up = self.pairs[current_index]
        while parent_index > 0:
            parent_index = self.__get_parent_index(current_index)
            if self.pairs[parent_index].priority < item_to_move_up.priority:
                self.pairs[current_index] = self.pairs[parent_index]
                current_index = parent_index
            else:
                break
        self.pairs[current_index] = item_to_move_up

    def __get_left_most_child_index(self, index: int) -> int:
        return self.arity * index + 1

    def __get_right_most_child_index(self, index: int) -> int:
        return self.arity * (index + 1)

    def __get_highest_priority_child_index(self, index: int) -> int:
        left_most_child_index = self.__get_left_most_child_index(index)
        right_most_child_index = self.__get_right_most_child_index(index)

        if left_most_child_index > len(self.pairs) - 1:
            return index

        if right_most_child_index > len(self.pairs) - 1:
            right_most_child_index = len(self.pairs) - 1

        indexes = range(left_most_child_index, right_most_child_index + 1)
        max_val = max(indexes, key=lambda i: self.pairs[i].priority)

        return max_val

    def __get_first_leaf_index(self) -> int:
        return ((len(self.pairs) - 2) // self.arity) + 1

    def __swap(self, first: int, second: int):
        second_el = self.pairs[second]
        self.pairs[second] = self.pairs[first]
        self.pairs[first] = second_el

    def __push_down(self, index: int = 0) -> None:
        current_index = index
        first_leaf_index = self.__get_first_leaf_index()
        el_to_push_down = self.pairs[index]

        while current_index < first_leaf_index:
            highest_pr_child_i = self.__get_highest_priority_child_index(current_index)
            highest_pr_child = self.pairs[highest_pr_child_i]
            if highest_pr_child.priority > el_to_push_down.priority:
                self.pairs[current_index] = self.pairs[highest_pr_child_i]
                current_index = highest_pr_child_i
            else:
                break

        self.pairs[current_index] = el_to_push_down

    def insert(self, content: str, priority: int) -> None:
        self.pairs.append(DHeapItem(content, priority))
        self.__bubble_up(len(self.pairs) - 1)

    def top(self) -> DHeapItem:

        if not any(self.pairs):
            raise EmptyHeapError()

        last = self.pairs.pop()

        if not any(self.pairs):
            return last

        top = self.pairs[0]
        self.pairs[0] = last
        self.__push_down(0)
        return top

    def peek(self) -> DHeapItem:
        return self.pairs[0]

    def update(self, value, priority):
        for i, v in enumerate(self.pairs):

            if v.value != value:
                continue

            old_pr = self.pairs[i].priority
            self.pairs[i].priority = priority
            if priority > old_pr:
                self.__bubble_up(i)
            elif priority < old_pr:
                self.__push_down(i)

    def __init__(self, pairs: List[DHeapItem] = None, arity=2):

        if arity is None:
            self.arity = 2
        else:
            self.arity = int(arity)

        if pairs is None:
            self.pairs: List[DHeapItem] = []
        else:
            self.pairs = list(pairs)
            self.__heapify()