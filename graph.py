#! /usr/bin/env python
#                print ' '.join(map( lambda x: x[0].__str__(), stack))

import sys, os
import pdb

class Node(object):
    LEFT, RIGHT, PARENT = 0, 1, 2
    def __init__(self, key, children = [], data= None, parent = None, color= None):
        self.data = data
        self.key = key
        self.children = children
        self.parent = parent
        self.color = color
    
    def __str__(self):
        return str(self.key)

    def isRoot(self):
        root = False if self.parent else True
        return root

class Tree(object):
    INORDER, PREORDER, POSTORDER = (0,1,2)
    def __init__(self, root =None, children=[]):
        self.root = root
        if self.root:
            self.root.children = children

    def insert(self, parent, node):
        if not self.root:
            self.root = node
        else:
            parent.children.append(node)
            parent.children[-1].parent = parent

    def progress(self, node, direction, constraint):
        if direction == Node.PARENT:
            while node and constraint(node):
                yield node
                node = node.parent
        else:
            while node and constraint(node):
                yield node
                node = node.children[direction]

    def DepthFS(self, start = None):
        current = start if start else self.root
        stack = [(current, 0)]
        yield current
        while len(stack):
            current, processed = stack.pop()
            while processed < len(current.children):
                stack.append((current, processed +1))
                for node in self.progress(current.children[processed], Node.LEFT, lambda x: x):
                    yield node
                    stack.append((node, 1))
                current, processed = stack.pop()

    def postorder(self, start = None):
#        pdb.set_trace()
        current = start if start else self.root
        stack = [(current, 0)]
        while len(stack):
            current, processed = stack.pop()
            while processed < len(current.children):
                stack.append((current, processed +1))
                for node in self.progress(current.children[processed], Node.LEFT, lambda x: x):
                    stack.append((node, 1)) 
#                print ' '.join(map( lambda x: x[0].__str__(), stack))
                current, processed = stack.pop()
            else:
                if processed == len(current.children):
                    yield current

    def inorder(self, start = None):
        current = start if start else self.root
        stack = [(current, 0)]
        while len(stack):
            current, processed = stack.pop()
            while processed < len(current.children):
                if processed == len(current.children)/2:
                    yield current
                stack.append((current, processed +1))
                for node in self.progress(current.children[processed], Node.LEFT, lambda x: x):
                    stack.append((node, 1)) 
                current, processed = stack.pop()

    def preorder(self, start = None):
        start = start if start else self.root
        for node in self.DepthFS(start):
           yield node
        
    def breadthFS(self, start = None):
        current = start if start else self.root
        q = Queue.Queue()
        q.put(curren)
        while not q.empty():
            current = q.get()
            for child in current.children:
                q.put(child)
                yield child

    def traverse(self, order):
        if order == Tree.INORDER:
            for node in self.inorder():
                yield node
        elif order == Tree.PREORDER:
            for node in self.preorder():
                yield node
        elif order == Tree.POSTORDER:
            for node in self.postorder():
                yield node
        
    def toString(self, order):
            return ' '.join([node.__str__() for node in self.traverse(order)])
            
    def __str__(self):
        return self.toString(Tree.INORDER)
    
    def __len__(self):
        return len([node for node in self.inorder()])

class BSTree(Tree):
    LEFT, RIGHT, PARENT = 0,1,2
    def __init__(self, root = None, children=[None, None]):
        if len(children) != 2 :
            print "Binary trees can not have less or more than children"
            sys.exit()
        super(BSTree,self).__init__(root, children)

    def insert(self, node):
        if not self.root:
            self.root = node
            return
        if len(node.children) !=2:
            print "Binary trees can not have less or more than children"
            sys.exit()
        current = self.root
        while current:
            if node.key >= current.key:
                if current.children[Node.RIGHT]:
                    current = current.children[Node.RIGHT]
                else:
                    current.children[Node.RIGHT] = node
                    node.parent = current
                    break
            else:
                if current.children[Node.LEFT]:
                    current = current.children[Node.LEFT]
                else:
                    current.children[Node.LEFT] = node
                    node.parent = current
                    break
        
    def search(self, key):
        current = self.root
        res = []
        while current:
            if key > current.key:
                    current = current.children[Node.RIGHT]
            elif key < current.key:
                    current = current.children[Node.LEFT]
            else:
                while current and key == current.key:
                    res.append(current)
                    current = current.children[Node.RIGHT]
                break
        return res
   

    def hasChild(self, node, direction):
        return node and node.children[direction]

    def isLeaf(self, node):
        return node and node.children and filter(lambda x: x, x.children)
    
    def __smallest(self, root):
            current = None
            for ptr in self.progress(root, Node.LEFT, lambda x: x):
                current = ptr
            return current
    
    def __largest(self, root):
            current = None
            for ptr in self.progress(root, Node.RIGHT, lambda x: x):
                current = ptr
            return current

    def isRoot(self, node):
        if node.parent:
            return False
        return True

    def isRightChild(self, node):
        return node == node.parent.children[Node.RIGHT]         

    def isLeftChild(self, node):
        return node == node.parent.children[Node.LEFT]         

    def successor(self, node):
        current = None
        if not node:
            return current

        if node.children[Node.RIGHT]: # right child exists, traverse the right subtree
            return self.__smallest(node.children[Node.RIGHT])
        else:
            if self.isRoot(node): #root case
                return None
            if self.isLeftChild(node): # left child with no right subree
                return node.parent
            #otherwise, traverse up till you find a parent with right subtree
            for ptr in self.progress(node, Node.PARENT, lambda x : x.parent and self.isRightChild(x)):
                current = ptr
            if current.parent:
                if current.parent.parent and self.isLeftChild(current.parent):
                    return current.parent.parent
            # we found that parent with right child
        return None

    def predecessor(self, node):
        current = None
        if not node:
            return current 
        if node.children[Node.LEFT]: # left child exists, traverse the left subtree
            return self.__largest(node.children[Node.LEFT])
        else:
            if self.isRoot(node): #root case
                return None
            if self.isRightChild(node): # left child with no right subree
                return node.parent
            #otherwise, traverse up till you find a parent with right subtree
            for ptr in self.progress(node, Node.PARENT, lambda x : x.parent and self.isLeftChild(x)):
                current = ptr
            if current.parent:
                if current.parent.parent and self.isRightChild(current.parent):
                    return current.parent.parent
            # we found that parent with right child
        return None        
         
            
def RBTree(BSTree):
    RED = 1
    BLACK = 0
    def __init__(self, root, children = [None, None]):
        root.color = RBTree.BLACK 
        super(RBTree, self).__init__(root, children)

    def insert(self, node):
        pass

    def delete(self, node):
        pass

if __name__ == "__main__":
    a1 = Node(1,[None, None])
    a2 = Node(2,[None, None])
    a3 = Node(3,[None, None])
    a4 = Node(4,[None, None])
    a5 = Node(5,[None, None])
    a52 = Node(5,[None, None])
    a6 = Node(6,[None, None])
    a7 = Node(7,[None, None])
    a8 = Node(8,[None, None])
    a9 = Node(9,[None, None])
    
    t = BSTree()
    t.insert(a5)
    t.insert(a3)
    t.insert(a2)
    t.insert(a4)
    t.insert(a52)
    t.insert(a7)
    t.insert(a9)
#    pdb.set_trace()
    print t
    print t.toString(Tree.PREORDER)
    print t.toString(Tree.POSTORDER)
    suc = t.search(9)[0]
    while suc:
        suc = t.predecessor(suc)
        print suc
