class TreeNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class SimpleBST:
    def __init__(self):
        self.root = None

    def insert(self, key, data=None):
        """Insert a new node."""
        new_node = TreeNode(key, data)
        if not self.root:
            self.root = new_node
        else:
            current = self.root
            while True:
                if key < current.key:
                    if current.left is None:
                        current.left = new_node
                        break
                    current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        break
                    current = current.right

    def display_inorder(self):
        """Display data in sorted order."""
        def inorder(node):
            if node:
                inorder(node.left)
                print(f"ID: {node.key}, Data: {node.data}")
                inorder(node.right)

        inorder(self.root)



bst = SimpleBST()
bst.insert(101, {"name": "Customer A"})
bst.insert(50, {"name": "Customer B"})
bst.insert(150, {"name": "Customer C"})

print("Customer Records:")
bst.display_inorder()






