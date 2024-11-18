import matplotlib.pyplot as plt

class RBNode:
    def __init__(self, value, color='red'):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()


class RedBlackTree:
    def __init__(self):
        self.root = None

    def search(self, value):
        curr_node = self.root
        while curr_node is not None:
            if value == curr_node.value:
                return curr_node
            elif value < curr_node.value:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return None

    def insert(self, value):
        new_node = RBNode(value)
        if self.root is None:
            self.root = new_node
        else:
            curr_node = self.root
            while True:
                if value < curr_node.value:
                    if curr_node.left is None:
                        curr_node.left = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.left
                else:
                    if curr_node.right is None:
                        curr_node.right = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.right
        self.insert_fix(new_node)

    def insert_fix(self, new_node):
        while new_node.parent and new_node.parent.color == 'red':
            if new_node.parent == new_node.grandparent().left:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_right(new_node.grandparent())
            else:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_left(new_node.grandparent())
        self.root.color = 'black'

    def delete(self, value):
        node_to_remove = self.search(value)
        if node_to_remove is None:
            return

        if node_to_remove.left is None or node_to_remove.right is None:
            self._replace_node(
                node_to_remove, node_to_remove.left or node_to_remove.right)
        else:
            successor = self._find_min(node_to_remove.right)
            node_to_remove.value = successor.value
            self._replace_node(successor, successor.right)

        self.delete_fix(node_to_remove)

    def delete_fix(self, node):
        while node != self.root and node.color == 'black':
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == 'red':
                    sibling.color = 'black'
                    node.parent.color = 'red'
                    self.rotate_left(node.parent)
                    sibling = node.parent.right

                if sibling.left.color == 'black' and sibling.right.color == 'black':
                    sibling.color = 'red'
                    node = node.parent
                else:
                    if sibling.right.color == 'black':
                        sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.rotate_right(sibling)
                        sibling = node.parent.right

                    sibling.color = node.parent.color
                    node.parent.color = 'black'
                    sibling.right.color = 'black'
                    self.rotate_left(node.parent)
                    node = self.root
        node.color = 'black'

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    def _replace_node(self, old_node, new_node):
        if old_node.parent is None:
            self.root = new_node
        else:
            if old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
        if new_node is not None:
            new_node.parent = old_node.parent

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def _inorder_traversal(self, node):
        if node is not None:
            self._inorder_traversal(node.left)
            print(node.value, end=" ")
            self._inorder_traversal(node.right)

    # Visualization function
    def visualize_tree(self):
        if self.root is None:
            print("Tree is empty.")
            return

        # Use Matplotlib to visualize the tree
        fig, ax = plt.subplots(figsize=(8, 8))
        self._plot_node(self.root, ax, 0, 0, 1)

        plt.show()

    def _plot_node(self, node, ax, x, y, width):
        if node is not None:
            ax.text(x, y, f'{node.value} ({node.color})', 
                    ha='center', va='center', color='black' if node.color == 'red' else 'white', 
                    fontsize=12, fontweight='bold', bbox=dict(facecolor=node.color, edgecolor='black', boxstyle='round,pad=0.5'))
            if node.left:
                ax.plot([x - width / 2, x], [y - 1, y], color='black', lw=1)
                self._plot_node(node.left, ax, x - width / 2, y - 1, width / 2)
            if node.right:
                ax.plot([x + width / 2, x], [y - 1, y], color='black', lw=1)
                self._plot_node(node.right, ax, x + width / 2, y - 1, width / 2)

# Example driver code
if __name__ == "__main__":
    tree = RedBlackTree()
    
    # Insert nodes
    for value in [10, 20, 30, 40, 50, 25]:
        tree.insert(value)

    print("Inorder traversal of the Red-Black Tree:")
    tree._inorder_traversal(tree.root)
    print()

    # Delete a node
    tree.delete(20)

    print("Inorder traversal of the Red-Black Tree after deleting 20:")
    tree._inorder_traversal(tree.root)
    print()

    # Visualize final tree
    tree.visualize_tree()
