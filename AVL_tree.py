"""
Based on the code provided at: https://github.com/laurentluce/python-algorithms/blob/master/algorithms/binary_tree.py
Extended to AVL trees by Karl Southern
"""
from tkinter import *


class Node:
    """
    Tree node: left and right child + data which can be any object
    """

    def __init__(self, data):
        """
        Node constructor

        :param data: node data object
        """
        self.left = None
        self.right = None
        self.data = data
        self.parent = None

    def lookup(self, data):
        """
        Lookup node containing data

        :param data: node data object to look up
        :returns: node if found
        :raise ValueError: data is not in tree
        """
        if data < self.data:
            if self.left is None:
                raise ValueError(f"{data} is not in tree")

            return self.left.lookup(data)

        if data > self.data:
            if self.right is None:
                raise ValueError(f"{data} is not in tree")

            return self.right.lookup(data)

        return self

    def __replace(self, with_node):
        """
        Replace this node's data and descendants with attributes from another node

        :param with_node: the node to take attributes from
        """
        self.left = with_node.left
        if self.left is not None:
            self.left.parent = self

        self.right = with_node.right
        if self.right is not None:
            self.right.parent = self

        self.data = with_node.data

    def refresh_parents(self):
        """
        Refresh the parents of all descendant nodes
        """
        if self.left is not None:
            self.left.parent = self
            self.left.refresh_parents()

        if self.right is not None:
            self.right.parent = self
            self.right.refresh_parents()

    def __no_children_delete(self):
        """
        Remove this node from the tree, assuming it has no children
        """
        # just remove it
        if not self.parent:
            del self
            return

        if self.parent.left is self:
            self.parent.left = None
        else:
            self.parent.right = None
        del self

    def __one_child_delete(self):
        """
        Remove this node from the tree, assuming it has exactly one child
        """
        # replace node with its child
        child = self.left or self.right
        self.__replace(child)

    def __two_children_delete(self):
        """
        Remove this node from the tree, assuming it has exactly two children
        """
        # find its successor: once to the right, then all the way left
        successor = self.right
        while successor.left is not None:
            successor = successor.left
        # replace node data by its successor data
        self.data = successor.data
        # fix successor's parent's child
        if successor.parent is self:
            self.right = successor.right
            if self.right:
                self.right.parent = self
            return

        successor.parent.left = successor.right
        if successor.parent.left:
            successor.parent.left.parent = successor.right

    def delete(self, data):
        """
        Delete node containing data

        :param data: node's content to delete
        :raise ValueError: data is not in tree
        """
        # get node containing data
        node = self.lookup(data)
        if node is None:
            raise ValueError("data is not in tree")

        children_count = node.children_count()
        if children_count == 0:
            node.__no_children_delete()
            return

        if children_count == 1:
            node.__one_child_delete()
            return

        node.__two_children_delete()

    def children_count(self):
        """
        Returns the number of children a node has

        :returns: number of children: 0, 1, 2
        """
        return int(self.left is not None) + int(self.right is not None)

    @classmethod
    def pre_order_traverse(cls, node):
        """
        Traverse a node's (sub)tree in pre-order

        :param node: the node whose (sub)tree you wish to traverse
        :return: an iterator that traverses the (sub)tree
        """
        yield node.data
        if node.left is not None:
            yield from cls.pre_order_traverse(node)
        if node.right is not None:
            yield from cls.pre_order_traverse(node)

    @classmethod
    def in_order_traverse(cls, node):
        """
        Traverse a node's (sub)tree in-order

        :param node: the node whose (sub)tree you wish to traverse
        :return: an iterator that traverses the (sub)tree
        """
        if node.left is not None:
            yield from cls.in_order_traverse(node)
        yield node.data
        if node.right is not None:
            yield from cls.in_order_traverse(node)

    @classmethod
    def post_order_traverse(cls, node):
        """
        Traverse a node's (sub)tree in post-order

        :param node: the node whose (sub)tree you wish to traverse
        :return: an iterator that traverses the (sub)tree
        """
        if node.left is not None:
            yield from cls.post_order_traverse(node)
        if node.right is not None:
            yield from cls.post_order_traverse(node)
        yield node.data

    def print_tree(self):
        """
        Print tree content inorder
        """
        data = list(self.in_order_traverse(self))
        print(data)

    def count_levels(self):
        """
        Count the number of levels in the tree
        """
        if (self.left is None) and (self.right is None):
            return 1

        if self.left is None:
            return self.right.count_levels() + 1

        if self.right is None:
            return self.left.count_levels() + 1

        left_count = self.left.count_levels()
        right_count = self.right.count_levels()

        return max(left_count, right_count) + 1

    def get_coords(self, x, y, sw, sh):
        to_send = [[x, y, self.data]]
        if self.left:
            to_send += (self.left.get_coords(x - sw / 2, y + sh, sw / 2, sh))
        if self.right:
            to_send += (self.right.get_coords(x + sw / 2, y + sh, sw / 2, sh))
        return to_send

    def get_lines(self, x, y, sw, sh):
        to_send = []
        if self.left:
            l = self.left.get_coords(x - sw / 2, y + sh, sw / 2, sh)
            to_send = to_send + [[x, y, l[0][0], l[0][1]]]
            to_send = to_send + self.left.get_lines(x - sw / 2, y + sh, sw / 2, sh)
        if self.right:
            r = self.right.get_coords(x + sw / 2, y + sh, sw / 2, sh)
            to_send = to_send + [[x, y, r[0][0], r[0][1]]]
            to_send = to_send + self.right.get_lines(x + sw / 2, y + sh, sw / 2, sh)
        return to_send

    def show_tree(self):
        self.refresh_parents()
        h = self.count_levels()
        w = 2 ** (h - 1)
        sh = 512 * 1.25
        sw = 512 * 1.5
        r = sw / w / 2
        if r >= 10:
            r = 10
        window = Tk()
        window.title("Binary Tree")  # Set a title
        canvas = Canvas(window, width=sw + 100, height=sh + 100, bg="white")
        canvas.pack()
        sh = int((sh - 2 * h * r) / h)
        toshow = self.get_lines(50 + sw / 2, 50 + r, sw / 2, sh)
        for i in toshow:
            x1 = i[0]
            y1 = i[1]
            x2 = i[2]
            y2 = i[3]
            canvas.create_line(x1, y1, x2, y2)
        toshow = self.get_coords(50 + sw / 2, 50 + r, sw / 2, sh)
        for i in toshow:
            x = i[0]
            y = i[1]
            text = i[2]
            if r == 10:
                canvas.create_oval(x - r, y - r, x + r, y + r, fill="white")
            canvas.create_text(x, y, text=text)

        window.mainloop()

    def insert(self, data):
        """
        Insert new node with data

        :param data: node data object to insert
        """
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                    self.left.parent = self
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                    self.right.parent = self
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def rotate_right(self):
        """
        rotate the tree to the right such that this node becomes the right child of the new root
        N.B you can't do self = new_root, so you will need to do:
        self.data = new_root.data
        self.left = new_root.left
        self.right = new_root.right
        self.parent = new_root.parent
        """
        new_root = Node(self.left.data)
        new_root.parent = self.parent
        old_root = Node(self.data)
        new_root.right = old_root
        old_root.parent = new_root
        old_root.left = self.left.right
        if old_root.left:
            old_root.left.parent = old_root
        old_root.right = self.right
        if old_root.right:
            old_root.right.parent = old_root
        new_root.left = self.left.left
        if new_root.left:
            new_root.left.parent = new_root

        self.data = new_root.data
        self.left = new_root.left
        if self.left:
            self.left.parent = self
        self.right = new_root.right
        if self.right:
            self.right.parent = new_root.right

    def rotate_left(self):
        """
        rotate the tree to the left such that this node becomes the left child of the new root
        N.B you can't do self = new_root, so you will need to do:
        self.data = new_root.data
        self.left = new_root.left
        self.right = new_root.right
        self.parent = new_root.parent
        """
        new_root = Node(self.right.data)
        new_root.parent = self.parent
        old_root = Node(self.data)
        new_root.left = old_root
        old_root.parent = new_root
        old_root.right = self.right.left
        if old_root.right:
            old_root.right.parent = old_root
        old_root.left = self.left
        if old_root.left:
            old_root.left.parent = old_root
        new_root.right = self.right.right
        if new_root.right:
            new_root.right.parent = new_root

        self.data = new_root.data
        self.right = new_root.right
        if self.right:
            self.right.parent = self
        self.left = new_root.left
        if self.left:
            self.left.parent = new_root.left

    #####################################################################################################
    #                                                                                                   #
    #                                EDIT THE CODE BELOW                                                #
    #                                                                                                   #
    #####################################################################################################

    # 1)Implement get_height
    # 2)Implement unbalanced
    # 3)Finish rebalance_inset and rebalance_delete
    # 4)Edit insert and delete to call the rebalance functions

    def get_height(self):
        """
        Should run on the node and return the height of the node.
        :return integer:
        """
        ...

    def unbalanced(self):
        """
        Should run on the node and return True if the subtree rooted at the node is unbalance, return False if
        the subtree rooted at this node is balanced.
        :return boolean:
        """
        ...

    def rebalance_insert(self):
        x = self
        if not x.parent:
            return
        y = x.parent
        if not y.parent:
            return
        z = y.parent
        while (not z.unbalanced()) and z.parent:
            (x, y, z) = (y, z, z.parent)
        if z.unbalanced():
            if z.left == y:
                if y.left == x:
                    # ll case
                    ...
                else:
                    # lr case
                    ...
            else:
                if y.right == x:
                    # rr case
                    ...
                else:
                    # rl case
                    ...
        # else done

    def rebalance_delete(self):
        z = self
        while (not z.unbalanced()) and z.parent:
            z = z.parent
        if z.unbalanced():
            zl = 0
            zr = 0
            if z.left:
                zl = z.left.get_height()
            if z.right:
                zr = z.right.get_height()
            if zl > zr:
                y = z.left
            else:
                y = z.right
            yl = 0
            yr = 0
            if y.left:
                yl = y.left.get_height()
            if y.right:
                yr = y.right.get_height()
            if yl > yr:
                x = y.left
            else:
                x = y.right

            if z.left == y:
                if y.left == x:
                    # ll case
                    ...
                else:
                    # lr case
                    ...
            else:
                if y.right == x:
                    # rr case
                    ...
                else:
                    # rl case
                    ...
        # else done
