from bisect import bisect_left
from collections import deque

class TrieNode(object):
    """
    Implemetns a simple tailored Trie node with following attributes  

    pointers: stores the mappings of the form (char->TrieNode)
    downWords: stores how many words are inserted in Trie rooted at this node.

    """
    def __init__(self):
        self.pointers={}
        self.downWords=0
#==================================
class Trie(object):
    """
    Implemetns a simple Trie of charachters data structure for efficient lookup of prefixes in a collection of strings.
    It implements two methods:
    insert(arg): inserts arg into Trie
    count_prefix(arg): returns how many words in the Trie have arg as their prefix.

    """

    def __init__(self):
        self.root=TrieNode()
        
    def insert(self, sentence):
        cur=self.root
        for char in sentence:
            if char not in cur.pointers:
                cur.pointers[char]=TrieNode()
                cur.pointers[char].downWords=1
            else:
                cur.pointers[char].downWords+=1
            cur=cur.pointers[char]
    
    def count_prefix(self,q_text):
        """
        Count how many questions in the trie have the q_text as prefix.

        """
        cur=self.root
        for char in q_text:
            if char not in cur.pointers:
                return 0
            else:
                cur=cur.pointers[char]       
        return cur.downWords
#==============================================================================================


    
class TopicNode(object):
    """
    TopicNode represents in node in topic graph. 

    topicName: is the name of topic 
    children: list of its children 
    question: a Trie to store and lookup efficiently questions associated with this topic.
    hashcode: hash of topic name. It is used purely for ease of lookup. One can use the actual string name for sorting the vertices

    It also implemets folowing methods.
    __gt__(other): comparison with other TopicNodes based on their hashcodes
    subtree(): generates the subtree rooted at this node (inclusive)


    """

    def __init__(self, topicName):
        self.topicName = topicName
        self.children = None
        self.hashcode = hash(topicName)
        self.question = Trie()
        
    def __gt__(self, other):
        return self.hashcode> other.hashcode
    
    def subtree(self):
        """Generator for subtree rooted at the node """
        queue= deque()
        queue.append(self)
        while(queue):
            current=queue.popleft()
            if current.children!=None:
                queue.extend(current.children)
            yield current

class TopicGraph(object):
    """
    This class implements the graph (tree) of topics. Every node in the graph is a TopicNode object.
    size: Number of nodees
    vertices: list of TopicNode nodes in the graph sorted by their hashcode
    """
    def __init__(self, N):
        self.size = N
        self.vertices = [None]*N 
       
    
    def buildTree(self,flatTree):
        """
        parses the flatTree string to build the tree.
        """

        raw = flatTree.strip().split(' ')
        par_stack=deque()
        child_stack=deque()
        
        current=TopicNode(raw[0])
        self.vertices[0]=current
        num_node_processed=1
        

        for idx in xrange(1,len(raw)):
            word=raw[idx]
            
            if word=='(':
                par_stack.append(current)
                
            elif word==')':
                parent=par_stack.pop()
                child= child_stack.pop()
                if parent.children==None:
                    parent.children=[child]
                else:
                    parent.children.append(child)
                    
                while(len(child_stack)!=0 and child_stack[-1]!=parent ):
                    child= child_stack.pop()
                    parent.children.append(child)
                    
            else:
                num_node_processed +=1
                current=TopicNode(word)
                self.vertices[num_node_processed-1]=current
                child_stack.append(current)
        
        self.vertices.sort()
        
    
    def find(self, topic):
        """ 
        locates the TopicNode given a string representing the node name
        """
        idx= bisect_left(self.vertices, TopicNode(topic))
        
        #Avoid hash collisions
        try:
            assert(self.vertices[idx].topicName == topic)
            return idx
        except:
            while(self.vertices[idx].topicName != topic and idx<self.size-1):
                idx+=1
                if self.vertices[idx].topicName == topic:
                    return idx
            else:
                raise KeyError('Topic not Found!!!')
            
    
    def addQuestions(self, information):
        """
        Add question to the the TopicNode
        """

        [topic,question]=information.split(': ')
        idx= self.find(topic)
        self.vertices[idx].question.insert( question )
      
    def countQueries(self,q):
        """
        traversing the subtree rooted at a given node and accumulate 
        how many questions in each childeren starts with a given query text.
        """

        topic, sentence = q.split(' ', 1)
        idx= self.find(topic)
        count = 0
        for node in self.vertices[idx].subtree():
            count+= node.question.count_prefix(sentence)
    
        return count

def main():
    N = int(raw_input().strip())
    T=TopicGraph(N)
    raw=raw_input().strip()
    T.buildTree(raw)
    M= int(raw_input().strip())
    for i in xrange(M):
        info= raw_input().strip()
        T.addQuestions(info)
    K= int(raw_input().strip())
    for i in xrange(K):
        q= raw_input().strip()
        print T.countQueries(q)

if __name__ == '__main__':
    main()