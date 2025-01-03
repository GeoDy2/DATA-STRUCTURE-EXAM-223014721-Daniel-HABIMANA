class TreeNode:
    def __init__(self, key, data=None):
        self.key = key  # Node identifier (e.g., department or category)
        self.data = data  # Associated data (e.g., customer group details)
        self.children = []  # List of child nodes

    def add_child(self, child_node):
        """Add a child node to the current node."""
        self.children.append(child_node)

    def display(self, level=0):
        """Display the tree hierarchy."""
        print(" " * (level * 4) + f"Key: {self.key}, Data: {self.data}")
        for child in self.children:
            child.display(level + 1)


class HierarchicalTree:
    def __init__(self):
        self.root = None

    def set_root(self, key, data=None):
        """Set the root of the tree."""
        self.root = TreeNode(key, data)

    def find_node(self, current, key):
        """Recursively find a node by key."""
        if current.key == key:
            return current
        for child in current.children:
            result = self.find_node(child, key)
            if result:
                return result
        return None

    def add_node(self, parent_key, key, data=None):
        """Add a node under a specified parent."""
        if not self.root:
            print("The tree has no root. Set the root first.")
            return
        parent_node = self.find_node(self.root, parent_key)
        if parent_node:
            parent_node.add_child(TreeNode(key, data))
        else:
            print(f"Parent node with key '{parent_key}' not found.")



crm_tree = HierarchicalTree()

# Setting the root node
crm_tree.set_root("Company", {"info": "Top Level"})

# Adding child nodes
crm_tree.add_node("Company", "Sales", {"info": "Handles sales operations"})
crm_tree.add_node("Company", "Support", {"info": "Customer support division"})
crm_tree.add_node("Sales", "Domestic", {"info": "Domestic sales team"})
crm_tree.add_node("Sales", "International", {"info": "International sales team"})

# Display the hierarchy
print("CRM Hierarchical Data:")
crm_tree.root.display()







