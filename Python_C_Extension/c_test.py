from random import randrange
import intervalTree   #C



def test(size):
    root = intervalTree.ITNode(500000,500002,500002)
    for i in range(size):
        low = randrange(1000000)
        high = randrange(low,1000000)
        node = intervalTree.ITNode(low,high,high)
        intervalTree.insert(root,node)
    intervalTree.overlapSearch(root,node)


if __name__ == "__main__":
    #test(10)
    test(1000)
    #test(100000)


"""
root = intervalTree.ITNode(0,10,10)
print 'root: ',root,'\n'
a = intervalTree.ITNode(11,20,20)
b = intervalTree.ITNode(3,30,30)
#print 'root address',root,'\n'
#print 'b address',b,'\n'
intervalTree.insert(root,a)
intervalTree.insert(root,b)
c =  intervalTree.ITNode(4,40,40)
intervalTree.insert(root,c)
c =  intervalTree.ITNode(5,50,50)
intervalTree.insert(root,c)
c =  intervalTree.ITNode(6,60,60)
intervalTree.insert(root,c)
c =  intervalTree.ITNode(3,40,40)
intervalTree.insert(root,c)
c =  intervalTree.ITNode(5,20,20)
intervalTree.insert(root,c)
print 'root address',root,'\n'
#print 'a right address',root.right,'\n'
#print a.max
#print 'b address',root.right.right,'\n'
#print b.max
#print intervalTree.overlapSearch(root,c)
"""
