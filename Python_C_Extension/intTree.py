from random import randrange

class ITNode:
    def __init__(self,low,high,max):
        self.low = low
        self.high = high
        self.max = max
        self.left = None
        self.right = None


def insert(root,node):
    if node.low < root.low:
        if root.left != None:
            insert(root.left, node)
        else:
            root.left = node
    else:
        if root.right != None:
            insert(root.right, node)
        else:
            root.right = node
    if (root.max < node.high):
        root.max = node.high


def doOverlap(node1,node2):
    if node1.low <= node2.high and node2.low <= node1.high:
        return 1
    return 0

def overlapSearch(root,node):
    if doOverlap(root,node):
        return root
    if root.left != None:
        return overlapSearch(root.left,node)
    elif root.right != None:
        return overlapSearch(root.right,node)
    else:
        return

