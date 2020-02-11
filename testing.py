from AVL_tree_complete import Node
root = Node(5)
toadd = [3,8,2,4,7,11,1,6,10,12,9,13]
#root = Node(4)
#toadd = [3,2,1,6,5]
for i in toadd:
    root.insert(i)
root.show_tree()
root.insert(14)
root.show_tree()
root.delete(5)
root.show_tree()
root.delete(4)
root.show_tree()
#root.print_tree()

