class Node:
    def __init__(self, data:any):
        self.data = data
        self.next:Node = None
        self.previous:Node = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    
