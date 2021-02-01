"""
Based on the code provided at: https://github.com/laurentluce/python-algorithms/blob/master/algorithms/binary_tree.py
Extended to AVL trees by Karl Southern
"""
from tkinter import *
import copy


class Node:
    """
    Tree node: left and right child + data which can be any object
    """

    def __init__(self, data):
        """
        Node constructor

        @param data node data object
        """
        self.left = None
        self.right = None
        self.data = data
        self.parent = None


    def lookup(self, data, parent=None):
        """
        Lookup node containing data

        @param data node data object to look up
        @param parent node's parent
        @returns node and node's parent if found or None, None
        """
        if data < self.data:
            if self.left is None:
                return None, None
            return self.left.lookup(data, self)
        elif data > self.data:
            if self.right is None:
                return None, None
            return self.right.lookup(data, self)
        else:
            return self, parent

    def refresh_parents(self):
        if self.left:
            self.left.parent = self
            self.left.refresh_parents()
        if self.right:
            self.right.parent = self
            self.right.refresh_parents()

    def delete(self, data):
        """
        Delete node containing data

        @param data node's content to delete
        """
        # get node containing data
        node, parent = self.lookup(data)
        if node is not None:
            children_count = node.children_count()
        if children_count == 0:
            # if node has no children, just remove it
            if parent:
                if parent.left is node:
                    parent.left = None
                else:
                    parent.right = None
                del node
            else:
                self.data = None
            parent.rebalance_delete()
        elif children_count == 1:
            # if node has 1 child
            # replace node with its child
            if node.left:
                n = node.left
            else:
                n = node.right
            if parent:
                n.parent = parent
                if parent.left is node:
                    parent.left = n
                else:
                    parent.right = n
                del node
            else:
                self.left = n.left
                if self.left:
                    self.left.parent = self
                self.right = n.right
                if self.right:
                    self.right.parent = self
                self.data = n.data
                self.parent = self.parent
                self.rebalance_delete()
        else:
            # if node has 2 children
            # find its successor
            parent = node
            successor = node.right
            while successor.left:
                parent = successor
                successor = successor.left
            # replace node data by its successor data
            node.data = successor.data
            # fix successor's parent's child
            if parent.left == successor:
                parent.left = successor.right
                if parent.left:
                    successor.right.parent = parent
            else:
                parent.right = successor.right
                if parent.right:
                    parent.right.parent = parent
            successor.rebalance_delete()

    def children_count(self):
        """
        Returns the number of children

        @returns number of children: 0, 1, 2
        """
        cnt = 0
        if self.left:
            cnt += 1
        if self.right:
            cnt += 1
        return cnt

    def print_tree(self):
        """
        Print tree content inorder
        """
        if self.left:
            self.left.print_tree()
        print(self.data),
        if self.right:
            self.right.print_tree()

    def count_levels(self):
        """
        Count the number of levels in the tree
        """
        lcount = 0
        rcount = 0
        if self.left:
            lcount = self.left.count_levels()
        if self.right:
            rcount = self.right.count_levels()
        return 1 + max(lcount, rcount)

    def get_coords(self, x, y, sw, sh):
        tosend = [[x, y, self.data]]
        if self.left:
            tosend = tosend + (self.left.get_coords(x - sw / 2, y + sh, sw / 2, sh))
        if self.right:
            tosend = tosend + (self.right.get_coords(x + sw / 2, y + sh, sw / 2, sh))
        return tosend

    def get_lines(self, x, y, sw, sh):
        tosend = []
        if self.left:
            l = self.left.get_coords(x - sw / 2, y + sh, sw / 2, sh)
            tosend = tosend + [[x, y, l[0][0], l[0][1]]]
            tosend = tosend + self.left.get_lines(x - sw / 2, y + sh, sw / 2, sh)
        if self.right:
            r = self.right.get_coords(x + sw / 2, y + sh, sw / 2, sh)
            tosend = tosend + [[x, y, r[0][0], r[0][1]]]
            tosend = tosend + self.right.get_lines(x + sw / 2, y + sh, sw / 2, sh)
        return tosend

    def show_tree(self):
        self.refresh_parents()
        h = self.count_levels()
        w = 2 ** (h - 1)
        sh = 512 * 1.25
        sw = 512 * 1.5
        r = sw / w / 2
        if r >=10:
            r = 10
        window = Tk()
        window.title("Binary Tree")  # Set a title
        canvas = Canvas(window, width=sw + 100, height=sh + 100, bg="white")
        canvas.pack()
        sh = int((sh - 2 * h * r) / (h))
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

        @param data node data object to insert

        """
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                    self.left.parent = self
                    self.left.rebalance_insert()
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                    self.right.parent = self
                    self.right.rebalance_insert()
                else:
                    self.right.insert(data)
        else:
            self.data = data
            self.rebalance_insert()

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

    ########################################################################################################################
    #                                                                                                                      #
    #                                          EDIT THE CODE BELOW                                                         #
    #                                                                                                                      #
    ########################################################################################################################
    """
    1)Implement get_height
    2)Implement unbalanced
    3)Finish rebalance_inset and rebalance_delete

    """
    def get_height(self):
        '''
        Should run on the node and return the height of the node.
        :return integer:
        '''
        l=0
        r=0
        if self.left:
            l=self.left.get_height()
        if self.right:
            r=self.right.get_height()
        return max(l,r)+1

    def unbalanced(self):
        '''
        Should run on the node and return True if the subtree rooted at the node is unbalance, return False if
        the subtree rooted at this node is balanced.
        :return boolean:
        '''
        l = 0
        r = 0
        if self.left:
            l = self.left.get_height()
        if self.right:
            r = self.right.get_height()
        if abs(l - r) > 1:
            return True
        return False

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
                    z.rotate_right()


                else:
                    # lr case
                    y.rotate_left()
                    z.rotate_right()

            else:
                if y.right == x:
                    # rr case
                    z.rotate_left()

                else:
                    # rl case
                    y.rotate_right()
                    z.rotate_left()
            z.refresh_parents()
            pass



    def rebalance_delete(self):
        z = self
        while (not z.unbalanced()) and z.parent:
            z = z.parent
        if z.unbalanced():
            zl = 0
            zr = 0
            if z.left:
                zl =z.left.get_height()
            if z.right:
                zr = z.right.get_height()
            if zl>zr:
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
                    z.rotate_right()


                else:
                    # lr case
                    y.rotate_left()
                    z.rotate_right()

            else:
                if y.right == x:
                    # rr case
                    z.rotate_left()

                else:
                    # rl case
                    y.rotate_right()
                    z.rotate_left()
                pass
            if z.parent:
                z.parent.rebalance_delete()



