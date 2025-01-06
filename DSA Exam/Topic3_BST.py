class TreeNode:
    def __init__(self, key, data=None):
        self.key = key  
        self.data = data  
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data=None):
        """Insert a new node into the BST."""
        new_node = TreeNode(key, data)
        if not self.root:
            self.root = new_node
        else:
            self._insert_recursively(self.root, new_node)

    def _insert_recursively(self, current, new_node):
        if new_node.key < current.key:
            if current.left is None:
                current.left = new_node
            else:
                self._insert_recursively(current.left, new_node)
        elif new_node.key > current.key:
            if current.right is None:
                current.right = new_node
            else:
                self._insert_recursively(current.right, new_node)
        else:
            print(f"Duplicate key '{new_node.key}' not allowed in BST.")

    def search(self, key):
        """Search for a node by key."""
        return self._search_recursively(self.root, key)

    def _search_recursively(self, current, key):
        if current is None:
            return None  
        if current.key == key:
            return current
        elif key < current.key:
            return self._search_recursively(current.left, key)
        else:
            return self._search_recursively(current.right, key)

    def inorder_traversal(self, node=None, result=None):
        """Perform an inorder traversal (sorted order)."""
        if node is None:
            node = self.root
        if result is None:
            result = []
        if node.left:
            self.inorder_traversal(node.left, result)
        result.append((node.key, node.data))
        if node.right:
            self.inorder_traversal(node.right, result)
        return result



crm_bst = BinarySearchTree()


crm_bst.insert(101, {"name": "Daniel", "email": "danielgeoffrey@example.com"})
crm_bst.insert(50, {"name": "Patrick", "email": "patrickniyo@example.com"})
crm_bst.insert(150, {"name": "Allan", "email": "allanrudas@example.com"})
crm_bst.insert(75, {"name": "Monique", "email": "moniqueuwase@example.com"})


search_key = 50
result = crm_bst.search(search_key)
if result:
    print(f"Customer found: {result.data}")
else:
    print(f"Customer with key {search_key} not found.")


print("Customer Records in Sorted Order:")
for key, data in crm_bst.inorder_traversal():
    print(f"ID: {key}, Data: {data}")



