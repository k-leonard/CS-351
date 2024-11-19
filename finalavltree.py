class AVLNode:
    def __init__(self, value):
        self.value = value  # The value will be used as the key as well
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    # Helper function to get the height of a node
    def height(self, node):
        return node.height if node else 0

    # Helper function to calculate the balance factor of a node
    def get_balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    # Right rotation
    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x

    # Left rotation
    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    # Insert a new value into the tree
    def insert(self, value):
        self.root = self._insert(self.root, value)

    # Recursive insert helper method
    def _insert(self, node, value):
        if not node:
            return AVLNode(value)

        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        # Balance the node
        balance = self.get_balance(node)

        # Left-Left case
        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)

        # Right-Right case
        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)

        # Left-Right case
        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right-Left case
        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # In-order traversal of the tree
    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.value, end=" ")
            self.inorder(root.right)

    # Public method to start in-order traversal
    def print_inorder(self):
        self.inorder(self.root)
        print()
    
    def search(self, key):
        return self._search_helper(self.root, key)

    # Recursive helper function for searching
    def _search_helper(self, node, key):
        if node is None:  # Base case: node not found
            return None

        if node.value == key:  # If the current node is the target
            return node

        elif key < node.value:  # If the target is smaller, search in the left subtree
            return self._search_helper(node.left, key)

        else:  # If the target is larger, search in the right subtree
            return self._search_helper(node.right, key)

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, root, value):
        if not root:
            return root

        # Find the node to delete
        if value < root.value:
            root.left = self._delete(root.left, value)
        elif value > root.value:
            root.right = self._delete(root.right, value)
        else:  # Node to be deleted found
            # Node with only one child or no child
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp

            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self._min_value_node(root.right)

            # Copy the inorder successor's content to this node
            root.value = temp.value

            # Delete the inorder successor
            root.right = self._delete(root.right, temp.value)

        # If the tree only has one node, return it
        if not root:
            return root

        # Update height of the current node
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Balance the tree
        balance = self.get_balance(root)

        # Left-Left case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Right-Right case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Left-Right case
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left case
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root
        
    def _min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self._min_value_node(node.left)


# Example Usage:
if __name__ == "__main__":
    tree = AVLTree()

    # Insert values into the AVL Tree
    values = [10, 20, 30, 15, 25, 5]
    for value in values:
        tree.insert(value)

    print("Inorder traversal of the AVL Tree:")
    tree.print_inorder()
