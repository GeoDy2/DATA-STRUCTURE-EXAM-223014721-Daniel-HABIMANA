class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = Node(data)
        if not self.head:  # If the list is empty
            self.head = new_node
            self.head.next = self.head  # Circular link
        else:
            temp = self.head
            while temp.next != self.head:  # Traverse to the last node
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head  # Maintain circular property

    def traverse(self):
        if not self.head:
            print("The list is empty.")
            return
        temp = self.head
        while True:
            print(temp.data, end=" -> ")
            temp = temp.next
            if temp == self.head:
                print("(back to head)")
                break


# Example
cll = CircularLinkedList()
cll.add("Customer1: Daniel")
cll.add("Customer2: Patrick")
cll.add("Customer3: Allan")
cll.traverse()


