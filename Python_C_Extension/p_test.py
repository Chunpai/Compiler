from random import randrange
import intTree        #Python


def test(size):
    root = intTree.ITNode(500000,500002,500002)
    for i in range(size):
        low = randrange(1000000)
        high = randrange(low,1000000)
        node = intTree.ITNode(low,high,high)
        intTree.insert(root,node)
    intTree.overlapSearch(root,node)

if __name__ == "__main__":
    #test(10)
    test(1000)
    #test(1000000)



"""
root = intervalTree.ITNode(0,10,10)
#print root
a = intervalTree.ITNode(11,20,20)
b = intervalTree.ITNode(3,30,30)
#print 'root address',root,'\n'
print 'b address',b,'\n'
intervalTree.insert(root,a)
intervalTree.insert(root,b)
print 'root address',root,'\n'
print root.max
print 'a right address',root.right,'\n'
print a.max
print 'b address',root.right.right,'\n'
print b.max
print intervalTree.overlapSearch(root,b)
"""
