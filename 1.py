"""
File: linkedbst.py
Author: Ken Lambert
"""

import time
import random
import math
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            part = ""
            if node is not None:
                part += recurse(node.right, level + 1)
                part += "| " * level
                part += str(node.data) + "\n"
                part += recurse(node.left, level + 1)
            return part

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    @staticmethod
    def preorder():
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    @staticmethod
    def postorder():
        """Supports a postorder traversal on a view of self."""
        return None

    @staticmethod
    def levelorder():
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            if item == node.data:
                return node.data
            if item < node.data:
                return recurse(node.left)
            return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            probe = probe.right
            if probe.data > item:
                probe = probe.left

        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * math.log(self._size + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        container = []
        for node in self:
            if low <= node <= high and node not in container:
                container.append(node)
                if low in container and high in container:
                    break
        return sorted(container)

    def rebalance_preparation(self, nodes_container):
        """
        This function helps the main rebalance function.
        """
        if not nodes_container:
            return None
        midle = len(nodes_container)//2
        node = nodes_container[midle]
        self.add(node)
        self.rebalance_preparation(nodes_container[:midle])
        self.rebalance_preparation(nodes_container[midle+1:])
        return self

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        if not self._root:
            return None

        nodes_container = []

        for num in self:
            nodes_container.append(num)
        nodes_container.sort()

        self.clear()

        return self.rebalance_preparation(nodes_container)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = None

        for num in self:
            # print(num)
            if num == item:
                continue
            if result is None and num > item:
                result = num
            if result is not None:
                if result > num > item:
                    result = num
        return result

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = None

        for num in self:
            if num == item:
                continue
            if result is None and num < item:
                result = num
            if result is not None:
                if result < num < item:
                    result = num
        return result

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        dictionary = []
        with open(path) as file:
            for word in file:
                dictionary.append(word[:-1])
        slovnyk = []
        # not sorted
        unsorted_tree = LinkedBST()
        list_of_not_sorted_words = []
        for i in range(900):
            word = random.choice(dictionary)
            slovnyk.append(word)
            unsorted_tree.add(word)
            list_of_not_sorted_words.append(word)

        # sorted
        sorted_tree = LinkedBST()
        list_of_sorted_words = dictionary[:900]
        for i in range(900):
            sorted_tree.add(dictionary[i])

        # balanced
        balanced_tree = LinkedBST()
        sorted_words = []
        for i in range(900):
            word = random.choice(dictionary)
            balanced_tree.add(word)
            sorted_words.append(word)
        balanced_tree.rebalance()

        start_time = time.monotonic()
        for _ in range(10000):
            word = random.choice(slovnyk)
            slovnyk.index(word)
        end_time = time.monotonic() - start_time
        print(
            f"This is overal searchtime for searching random \
word from the dictionary in the list of 900 words -> {end_time}")

        def find(tree, item):
            """If item matches an item in self, returns the
            matched item, or None otherwise."""
            def recurse(node):
                if node is None:
                    return None
                if item == node.data:
                    return node.data
                if item < node.data:
                    return recurse(node.left)
                return recurse(node.right)
            return recurse(tree._root)

        start_time = time.monotonic()
        for _ in range(10000):
            word = random.choice(list_of_not_sorted_words)
            find(unsorted_tree, word)

        end_time = time.monotonic() - start_time
        print(
            f"\n\n\nThis is overal searchtime for searching random \
word from the dictionary in the binary tree of 900 words -> {end_time}")

        start_time = time.monotonic()
        for _ in range(10000):
            word = random.choice(list_of_sorted_words)
            find(sorted_tree, word)

        end_time = time.monotonic() - start_time
        print(
            f"\n\n\nThis is overal searchtime for searching random word \
from the dictionary in the sorted binary tree of 900 words -> {end_time}")

        start_time = time.monotonic()
        for _ in range(10000):
            word = random.choice(sorted_words)
            find(balanced_tree, word)

        end_time = time.monotonic() - start_time
        print(
            f"\n\n\nThis is overal searchtime for searching random word \
from the dictionary in the balanced binary tree of 900 words -> {end_time}")


if __name__ == "__main__":
    bst = LinkedBST()
    for el in [2, -1, 3, 4, 4, -2, 6, 6, 10, -32]:
        bst.add(el)
    print(bst.demo_bst("words.txt"))
