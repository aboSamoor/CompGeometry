#! /usr/bin/env python

import sys, os
import pdb
import Queue

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

    def isLeaf(self, node):
        return not reduce(lambda x,y: x or y, node.children)
    
    def delete(self, node):
        pass

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
#        pdb.set_trace()
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
        q.put(current)
        while not q.empty():
            current = q.get()
            for child in current.children:
                q.put(child)
                yield child

    def traverse(self, order):
        if not self.root:
            yield None
        elif order == Tree.INORDER:
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
            if node.isRoot(): #root case
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
            if node.isRoot(): #root case
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

    def updateParent(self, node, parent):
        for child in filter(lambda x:x, node.children):
                    child.parent = parent

    def delete(self, node): 
        if self.isLeaf(node):
            if not node.isRoot():
                node.parent.children[node.parent.children.index(node)] = None
            else:
                self.root = None
        else:
            succ = self.successor(node)
            if succ:
                    if succ.isRoot():
                        succ.children[Node.LEFT] = node.children[Node.LEFT]
                        self.updateParent(node, succ)
                    else:
                        succ.children[Node.LEFT] = node.children[Node.LEFT]
                        succ.parent.children[succ.parent.children.index(succ)] = succ.children[Node.RIGHT]
                        succ.children[Node.RIGHT] = node.children[Node.RIGHT]
                        self.updateParent(node, succ)
                        if node.isRoot():
                            self.root = succ
                            succ.parent = None
                        else:
                            node.parent.children[node.parent.children.index(node)] = succ
                            succ.parent = node.parent
            else:
                pre = self.predecessor(node)
                if pre:
                    if pre.isRoot():
                        pre.children[Node.RIGHT] = node.children[Node.RIGHT]
                        self.updateParent(node, pre)
                    else:
                        pre.children[Node.RIGHT] = node.children[Node.RIGHT]
                        pre.parent.children[pre.parent.children.index(pre)] = pre.children[Node.LEFT]
                        pre.children[Node.LEFT] = node.children[Node.LEFT]
                        self.updateParent(node, succ)
                        if node.isRoot():
                            self.root = pre
                            pre.parent = None
                        else:
                            node.parent.children[node.parent.children.index(node)] = pre
                            pre.parent = node.parent
                else:
                    print "An error happened, no succ or pre and still not a leaf", node

            
class RBTree(BSTree):
    RED, BLACK = 1, 0
    def __init__(self, root, children = [None, None]):
        root.color = RBTree.BLACK 
        super(RBTree, self).__init__(root, children)

    def insert(self, node):
        pass

    def delete(self, node):
        pass



class Heap(Tree):
    def __init__(self):
        super(Heap, self).__init__()
        self.nodes = []
    def __parent(self, pos):
        parent = (pos-1)/2 if (pos-1)/2 != -1 else None
        return parent
    def __leftChild(self, pos):
        left = 2*pos + 1 if 2*pos+1 < len(self.nodes) else None
        return left
    def __rightChild(self, pos):
        right = 2*pos + 2 if 2*pos+2 < len(self.nodes) else None
        return right
    def __updatePtrs(self, pos):
        if pos == None:
            return 0
        left = self.__leftChild(pos)
        right = self.__rightChild(pos)
        parent = self.__parent(pos)
        if left!= None:
            self.nodes[pos].children[BSTree.LEFT] = self.nodes[left]
            self.nodes[left].parent = self.nodes[pos]
        else:
            self.nodes[pos].children[BSTree.LEFT] = None
            
        if right!= None:
            self.nodes[pos].children[BSTree.RIGHT] = self.nodes[right]
            self.nodes[right].parent = self.nodes[pos]
        else:
            self.nodes[pos].children[BSTree.RIGHT] = None
        
        if parent != None:
            self.nodes[pos].parent = self.nodes[parent]
            if self.__leftChild(parent) == pos:
                self.nodes[parent].children[BSTree.LEFT] = self.nodes[pos]
            elif self.__rightChild(parent) == pos:
                self.nodes[parent].children[BSTree.RIGHT] = self.nodes[pos]
        else:
            self.nodes[pos].parent = None

    def __swap(self, pos, pos2):
        self.nodes[pos], self.nodes[pos2] = self.nodes[pos2], self.nodes[pos]
        self.__updatePtrs(pos)
        self.__updatePtrs(pos2)
        if pos*pos2 == 0:
            self.root = self.nodes[0]
        
    def __bubbleUp(self):
        pos = len(self.nodes) - 1
        parent = self.__parent(pos)
        while  parent != None and self.nodes[pos].key < self.nodes[parent].key:
            self.__swap(pos, self.__parent(pos))
            pos = parent
            parent = self.__parent(pos)
    def __isLeaf(self, pos):
        return self.__leftChild(pos)== None and self.__rightChild(pos)== None
    
    def __bubbleDown(self):
        pos = 0
        lastPos = -1
        while not self.isLeaf(self.nodes[pos]) and lastPos != pos:
            left = self.__leftChild(pos)
            right = self.__rightChild(pos)
            lastPos = pos
            poss = filter(lambda x: x, [left, right])
            keys = map(lambda x: (self.nodes[x].key, x), poss)
            minKey, minPos = min(keys) if keys else (None, None)
            if minPos != None and self.nodes[minPos].key < self.nodes[pos].key:
                self.__swap(pos, minPos)
                pos = minPos

    def insert(self,node):
        self.nodes.append(node)
        self.__updatePtrs(len(self.nodes) -1)
        self.__updatePtrs(self.__parent(len(self.nodes)-1))
        if not self.root:
            self.root = self.nodes[0]
        self.__bubbleUp()
    def __delete(self):
        end = len(self.nodes)-1
        del self.nodes[end]
        if len(self.nodes) ==0:
            self.root = None
        self.__updatePtrs(self.__parent(end))
        
    def extract_min(self):
        if len(self.nodes) == 0:
            return None
        res = self.nodes[0]
        self.__swap(0, len(self.nodes)-1)
        self.__delete()
        if len(self.nodes):
            self.__bubbleDown()
        return res
    def merge(self, heap2):
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
    
    t = Heap()
    t.insert(a5)
    t.insert(a3)
    t.insert(a2)
    t.insert(a4)
    t.insert(a8)
    t.insert(a7)
    t.insert(a9)
#    pdb.set_trace()
#    print t
    print t
    print t.extract_min()
    print t
    print t.extract_min()
    print t
    print t.extract_min()
    print t
    print t.extract_min()
    print t
    print t.extract_min()
    print t
    print t.extract_min()
    print t
    print t.extract_min()
    print t