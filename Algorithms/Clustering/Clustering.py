import re
import sys
import operator
import heapq
from heapq import *
import itertools
from collections import defaultdict
import unittest


INF = float('inf')

class Priority_Queue:
	
	#Adapted from another's code
	def __init__(self):
		self.pq = []
		self.entry_finder = {}
		self.REMOVED = '<removed-task>'
		self.counter = itertools.count()
	
	def __getitem__(self, x):
		return self.entry_finder[indx]
	
	def __len__(self):#Items with self.Removed should not be counted
		count = 0
		for x in self.pq:
			priority, head, msg = x
			if msg != self.REMOVED:
				count += 1
		return count
	
	def add_task(self, task, priority=0):#Adds item to heap; if it exists, it is set to removed and the new item is added;
		if task in self.entry_finder:
			self.remove_task(task)
		count = next(self.counter)
		entry = [priority, count, task]
		self.entry_finder[task] = entry
		heappush(self.pq, entry)#First element of entry determines position in heap

	def remove_task(self, task):
		entry = self.entry_finder.pop(task)
		entry[-1] = self.REMOVED #set the task to removed,
	
	def pop_task(self):#Release the lowest item in the heap
		while self.pq:
			priority, count, task = heappop(self.pq)
			if task is not self.REMOVED:#Do not pop removed tasks
				del self.entry_finder[task]#Remove it from the queue
				return task, priority
		raise KeyError('pop from an empty priority queue')

INF = float("inf")

class Explicit(object):
    
    def __init__(self, name, edges):
        self.name = name
        self.distances = dict(edges)
    
    def __str__(self):
        return "Node{0}".format(self.name)


    def get_dist(self, other):
        if self.distances.has_key(other.name):
            return self.distances[other.name]
        else: return INF

class Implicit(object):
    
    def __init__(self, name, form):
        self.name = name
        self.form = int(''.join(form.split(" ")),2)

    def __str__(self):
       return "Node{0}:{1}".format(self.name, self.form)

    def get_dist(self, other): #Hamming distance
        if self.form == other.form: 
            return 0
        else:
            return bin(self.form ^ other.form).count('1')

class UnionFind(object):

    def __init__(self, nodes):
        self.sizes = {}
        self.clusters = {}
        for node in nodes:
            self.clusters[node.name] = node.name
            self.sizes[node.name] = 1
    
    def __str__(self):
        return str(sorted([(self.sizes[key], key) for key in self.sizes.keys()], reverse=True)[0:5])


    def __len__(self):
        return len(self.sizes)    

    def find(self, node):
        return self.clusters[node]


    def union(self, u, v):
        u_size = self.sizes[self.clusters[u]]
        v_size = self.sizes[self.clusters[v]]
        if u_size  >= v_size:
           new_leader = self.clusters[u]
           old_leader = self.clusters[v]
        else: 
            new_leader = self.clusters[v]
            old_leader = self.clusters[u] 
        
        new_size = u_size + v_size
        #print "Deleting ", old_leader
        del self.sizes[old_leader]
        self.sizes[new_leader] = new_size
        for key in self.clusters.keys():
            if self.clusters[key] == old_leader:
               self.clusters[key] = new_leader
          
        
class Clustering(object):


    def __init__(self):
        self.nodes = []
        self.queue = Priority_Queue()
       
    def explicit(self, lines):
        self.edges = defaultdict(list)
        for line in lines:
             numbers = [int(x) for x in re.findall('[0-9]+', line)]
             x = int(numbers[0])
             y = int(numbers[1])
             d = int(numbers[2])
             self.edges[x].append((y, d))
             self.edges[y].append((x, d))
        for key in self.edges.keys():
             node = Explicit(key, self.edges[key])
             self.nodes.append(node)
             for edge in self.edges[key]:
                 y, d = edge
                 self.queue.add_task((key, y), priority=d)

    def implicit(self, lines):
       
        for i, line in enumerate(lines):
            node = Implicit(name=int(i), form=line)
            self.nodes.append(node)
        explicit_nodes = {}
        for node in self.nodes:
            viable_nodes = [(nodeB.name, nodeB.get_dist(node)) for nodeB in self.nodes if nodeB.get_dist(node) <=3]
            explicit_nodes[node.name] = viable_nodes
        self.nodes = []
        for key in explicit_nodes.keys():
            node = Explicit(key, explicit_nodes[key])
            self.nodes.append(node)
            for edge in explicit_nodes[key]:
                y, d = edge
                self.queue.add_task((key, y), priority=d)

        print len(self.nodes), " nodes"
        print self.nodes[0], "queue ", len(self.queue)

    def min_distance(self):
        if type(self.extract_min())==None: return self.min_dist
        else: return self.extract_min()[0]

    def cluster_count(self):
        return len(self.clusters)


    def extract_min(self):
        return min([(nodeA.get_dist(nodeB), nodeA.name, nodeB.name) for nodeA in self.nodes for nodeB in self.nodes if self.clusters.find(nodeB.name) != self.clusters.find(nodeA.name)])
       
    def get_min(self):
        same_cluster = True
        while same_cluster == True:
            (x, y), dist = self.queue.pop_task()
            same_cluster = self.clusters.find(x) == self.clusters.find(y)
        return (dist, x,y)    

    def get_min_dist(self):
        if len(self.queue) == 0: return self.min_dist
        else: return self.get_min()[0]


    def main(self, k, f):
        self.clusters = UnionFind(self.nodes)
        within_dist = True
        while len(self.clusters) > k and within_dist:
             self.min_dist, a, b = self.get_min()
             within_dist = f(self.min_dist)
             if within_dist: self.clusters.union(a,b)




class TestTests(unittest.TestCase):
    
    def setUp(self):
        pass   
    
    def test_explicit_one(self):
        self.c = Clustering()
        glines = "1 2 134365\n1 3 847434\n1 4 763775\n1 5 255070\n1 6 495436\n1 7 449492\n1 8 651593\n1 9 788724\n1 10 93860\n2 3 28348\n2 4 835766\n2 5 432768\n2 6 762281\n2 7 2107\n2 8 445388\n2 9 721541\n2 10 228763\n3 4 945271\n3 5 901428\n3 6 30590\n3 7 25446\n3 8 541413\n3 9 939150\n3 10 381205\n4 5 216600\n4 6 422117\n4 7 29041\n4 8 221692\n4 9 437888\n4 10 495813\n5 6 233085\n5 7 230867\n5 8 218782\n5 9 459604\n5 10 289782\n6 7 21490\n6 8 837578\n6 9 556455\n6 10 642295\n7 8 185907\n7 9 992544\n7 10 859947\n8 9 120890\n8 10 332696\n9 10 721485".split("\n")
        self.c.explicit(glines)
        self.c.main(k=4, f=lambda a: a > 0)
        self.assertTrue(self.c.get_min_dist()==134365)

    def test_explicit_two(self):
        self.c = Clustering()
        glines = "1 2 1\n1 3 3\n1 4 8 \n1 5 12\n1 6 13\n2 3 2\n2 4 14\n2 5 11\n2 6 10\n3 4 15\n3 5 17\n3 6 16\n4 5 7\n4 6 19\n5 6 9".split("\n")
        self.c.explicit(glines)
        self.c.main(k=4, f=lambda a: a > 0) 
        self.assertTrue(self.c.get_min_dist()==7)

    def test_implicit_dist(self):
        v = Implicit(1, "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1")
        u = Implicit(2, "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1")
        self.assertTrue(v.get_dist(u)==3)


    def test_implicit_one(self):
        self.c = Clustering()
        glines = "1 1 1 0 0 0 0\n1 1 0 0 0 0 0\n1 0 1 0 0 0 1\n0 0 0 1 1 1 1\n0 0 0 1 0 1 1\n1 0 1 1 0 1 1".split("\n")
        self.c.implicit(glines)
        self.c.main(k=1, f=lambda a: a <= 3)
        print "CLUSTER COUNT ", self.c.cluster_count(), "\n", self.c.clusters
        self.assertTrue(self.c.cluster_count()==1)
    
    def test_implicit_two(self):
        self.c = Clustering()
        glines = "1 1 0 0 1 0 0 0\n0 0 1 1 1 1 1 1\n1 0 1 0 1 0 0 1\n0 0 1 0 0 1 1 0\n1 0 1 0 1 1 1 0\n1 1 0 1 1 0 1 1\n1 0 1 0 0 1 1 1\n1 1 1 0 0 1 0 0\n0 0 0 0 0 0 0 1\n0 1 0 0 0 1 1 0\n1 1 0 0 0 0 0 0\n1 0 0 1 0 1 1 0\n0 0 1 1 1 1 1 0\n0 0 1 0 1 0 1 1\n0 0 0 1 1 1 1 0".split("\n")
        self.c.implicit(glines)
        self.c.main(k=1, f=lambda a: a <= 2)
        print "CLUSTER COUNT ", self.c.cluster_count()
        self.assertTrue(self.c.cluster_count()==4) 


if __name__ == '__main__':
    try:
        etext = file(sys.argv[1], 'r')
        itext = file(sys.argv[2], 'r')
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    elines = etext.readlines()[1:]
    ilines = itext.readlines()[1:]
    c = Clustering()
    c.explicit(elines)
    c.main(k=4, f = lambda a: a > 0)
    print "Explicit nodes {0}".format(c.min_distance())
    c = Clustering()
    c.implicit(ilines)
    c.main(k=1, f= lambda a: a < 3)
    print "Implicit nodes {0}".format(c.cluster_count()) 


"""
if __name__ == '__main__':
   unittest.main()
"""


