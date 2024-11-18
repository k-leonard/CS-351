class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # height of the node

class AVLTree:
    # Get the height of the node
    @staticmethod
    def height(N):
        if N is None:
            return 0
        return N.height

    # Right rotation
    @staticmethod
    def right_rotate(y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = max(AVLTree.height(y.left), AVLTree.height(y.right)) + 1
        x.height = max(AVLTree.height(x.left), AVLTree.height(x.right)) + 1

        # Return new root
        return x

    # Left rotation
    @staticmethod
    def left_rotate(x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = max(AVLTree.height(x.left), AVLTree.height(x.right)) + 1
        y.height = max(AVLTree.height(y.left), AVLTree.height(y.right)) + 1

        # Return new root
        return y

    # Get the balance factor of the node
    @staticmethod
    def get_balance(N):
        if N is None:
            return 0
        return AVLTree.height(N.left) - AVLTree.height(N.right)

    # Insert a new key in the AVL tree
    @staticmethod
    def insert(node, key):
        # 1. Perform the normal BST insertion
        if node is None:
            return Node(key)

        if key < node.key:
            node.left = AVLTree.insert(node.left, key)
        elif key > node.key:
            node.right = AVLTree.insert(node.right, key)
        else:  # Duplicate keys not allowed
            return node

        # 2. Update height of this ancestor node
        node.height = max(AVLTree.height(node.left), AVLTree.height(node.right)) + 1

        # 3. Get the balance factor of this node
        balance = AVLTree.get_balance(node)

        # If this node becomes unbalanced, then there are 4 cases

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return AVLTree.right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return AVLTree.left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = AVLTree.left_rotate(node.left)
            return AVLTree.right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = AVLTree.right_rotate(node.right)
            return AVLTree.left_rotate(node)

        return node

    # Find the node with the smallest value
    @staticmethod
    def min_value_node(node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Delete a node from the AVL tree
    @staticmethod
    def delete_node(root, key):
        # STEP 1: PERFORM STANDARD BST DELETE
        if root is None:
            return root

        # If the key to be deleted is smaller than the root's key
        if key < root.key:
            root.left = AVLTree.delete_node(root.left, key)

        # If the key to be deleted is greater than the root's key
        elif key > root.key:
            root.right = AVLTree.delete_node(root.right, key)

        # If key is same as root's key, then this is the node to be deleted
        else:
            # Node with only one child or no child
            if root.left is None or root.right is None:
                temp = root.left if root.left else root.right

                if temp is None:  # No child case
                    root = None
                else:  # One child case
                    root = temp

            else:
                # Node with two children: Get the inorder successor (smallest in right subtree)
                temp = AVLTree.min_value_node(root.right)

                # Copy the inorder successor's data to this node
                root.key = temp.key

                # Delete the inorder successor
                root.right = AVLTree.delete_node(root.right, temp.key)

        # STEP 2: UPDATE HEIGHT OF CURRENT NODE
        if root is None:
            return root

        root.height = max(AVLTree.height(root.left), AVLTree.height(root.right)) + 1

        # STEP 3: GET THE BALANCE FACTOR OF THIS NODE
        balance = AVLTree.get_balance(root)

        # If this node becomes unbalanced, then there are 4 cases
        if balance > 1 and AVLTree.get_balance(root.left) >= 0:
            return AVLTree.right_rotate(root)

        if balance > 1 and AVLTree.get_balance(root.left) < 0:
            root.left = AVLTree.left_rotate(root.left)
            return AVLTree.right_rotate(root)

        if balance < -1 and AVLTree.get_balance(root.right) <= 0:
            return AVLTree.left_rotate(root)

        if balance < -1 and AVLTree.get_balance(root.right) > 0:
            root.right = AVLTree.right_rotate(root.right)
            return AVLTree.left_rotate(root)

        return root

    # Preorder traversal
    @staticmethod
    def pre_order(root):
        if root is not None:
            print("{0} ".format(root.key), end="")
            AVLTree.pre_order(root.left)
            AVLTree.pre_order(root.right)

# Driver Code
if __name__ == "__main__":
    root = None

    # Insert nodes into the AVL Tree
    root = AVLTree.insert(root, 9)
    root = AVLTree.insert(root, 5)
    root = AVLTree.insert(root, 10)
    root = AVLTree.insert(root, 0)
    root = AVLTree.insert(root, 6)
    root = AVLTree.insert(root, 11)
    root = AVLTree.insert(root, -1)
    root = AVLTree.insert(root, 1)
    root = AVLTree.insert(root, 2)

    print("Preorder traversal of the constructed AVL tree is")
    AVLTree.pre_order(root)

    # Delete a node from the tree
    root = AVLTree.delete_node(root, 10)

    print("\nPreorder traversal after deletion of 10")
    AVLTree.pre_order(root)
