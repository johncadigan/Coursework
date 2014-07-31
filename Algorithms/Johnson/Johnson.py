import re, sys, operator
from collections import defaultdict
import heapq
import itertools
from heapq import *
from datetime import *
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
		


class Dijkstra(object):

	def __init__(self, vertices, tail_edges, target_edges, edge_distance):
		
		self.vertices = vertices
		self.edge_distance = edge_distance
		self.target_edges = target_edges#Get the target by the source vertex
	
	def pq_dijkstras(self, initial= None):
		if initial == None: initial = self.vertices[0]
		PQ = Priority_Queue()
		dist = {}
		for v in self.vertices: #Default dist to inf
			dist[v] = INF
			PQ.add_task(v, priority = INF)
		dist[initial] = 0
		while len(PQ) > 0:
			u = PQ.pop_task()#The vertex closest to the initial vertex
			u, priority = u
			for v in self.target_edges[u]:
				alt = dist[u] + self.edge_distance[(u,v)]
				if alt < dist[v]:#If a faster path is found, update the results
					dist[v] = alt
					PQ.add_task(v, priority = alt) #Update the score for the vertex; The previous score will be labeled with self.REMOVED.
		return dist
		
					
			
	
	def main(self, source):
            return self.pq_dijkstras(source)


class BellmanFord(object):

     def __init__(self, vertices, tail_edges, target_edges, edge_distance):
          self.vertices = vertices
          self.tail_edges = tail_edges #Get the sources by target vertex
          self.target_edges = target_edges #Get target by source vertex
          self.edge_distance = edge_distance

     @classmethod
     def from_lines(cls, lines):
          vertices = set([])
          edge_distance = {}
	  target_edges = defaultdict(list)
          tail_edges = defaultdict(list)
	  for line in lines[1:]:
	      numbers = [int(x.strip()) for x in  line.split(" ")]
              x = numbers[0]
              vertices.add(x)#Add source to vertices
              y = numbers[1]
              vertices.add(y)
              l = numbers[2]
              edge_distance[(x,y)] = l
              target_edges[x].append(y)
              tail_edges[y].append(x)
          vertices = list(vertices)
          vertices.sort()
          vertices_no, edges_no = [int(x) for x in lines[0].split(" ")]
          print "Checking... Vertices correct:{0} Edges correct:{1}".format(vertices_no==len(vertices), edges_no == len(edge_distance))
          return BellmanFord(vertices, tail_edges, target_edges, edge_distance)

     def main(self, source):
         A = defaultdict(dict)
         A[0] = {x: INF for x in self.vertices}
         A[0][source] = 0
         i = 1
         unrepeated = True
         while i < len(self.vertices) and unrepeated:
             for v in self.vertices:
                 possible = [w for w in self.tail_edges[v]]
                 current = A[i-1][v]
                 if len(possible) > 0:
                     min_possible = min([A[i-1][w] + self.edge_distance[(w,v)] for w in self.tail_edges[v]])
                     A[i][v] = min(current, min_possible)
                 else:
                     A[i][v] = current
             if A[i-1] == A[i]: unrepeated = False
             i+=1
         #Test for negative cycle by running one more time
         for v in self.vertices:
             possible = [w for w in self.tail_edges[v]]
             current = A[i-1][v]
             if len(possible) > 0:
                 min_possible = min([A[i-1][w] + self.edge_distance[(w,v)] for w in self.tail_edges[v]])           
                 A[i][v] = min(current, min_possible)
             else:
                 A[i][v] = current
         if A[i-1] == A[i]: 
             return A[i-1]
         else:
             return None
         
                      
     
class Johnson(object):
      
      def __init__(self, lines):
           self.vertices = set([])
           self.edge_distance = {}
	   self.target_edges = defaultdict(list)
           self.tail_edges = defaultdict(list)
	   for line in lines[1:]:
	       numbers = [int(x.strip()) for x in  line.split(" ")]
               x = numbers[0]
               self.vertices.add(x)#Add source to vertices
               y = numbers[1]
               self.vertices.add(y)
               l = numbers[2]
               self.edge_distance[(x,y)] = l
               self.target_edges[x].append(y)
               self.tail_edges[y].append(x)
           self.vertices = list(self.vertices)
           self.vertices.sort()
           vertices_no, edges_no = [int(x) for x in lines[0].split(" ")]
           print "Checking... Vertices correct:{0} Edges correct:{1}".format(vertices_no==len(self.vertices), edges_no == len(self.edge_distance))


      
      def run_bf(self):
           bf_vertices = list(self.vertices)
           bf_vertices.append('s')
           bf_edge_distance = dict(self.edge_distance)
           bf_tail_edges = dict(self.tail_edges)
           bf_target_edges = dict(self.target_edges)
           for v in bf_vertices:
               bf_edge_distance[('s',v)] = 0
               if bf_tail_edges.has_key(v) == False: bf_tail_edges[v] = []
               bf_tail_edges[v].append('s')
           bf = BellmanFord(bf_vertices, bf_tail_edges, bf_target_edges, bf_edge_distance)
           self.p = bf.main('s')#Minimum distances to be used to create G' and calculate final distances
      
      def create_reweighted_edges(self):
          recalculated_edges = {} 
          for e in self.edge_distance.keys():
              x,y = e
              recalculated_edges[(x,y)] = self.edge_distance[e] + self.p[x] - self.p[y]
          return recalculated_edges

      def calculate_correct_distances(self, distances):
          correct_distances = defaultdict(dict)
          self.min_dist = INF
          for u in distances.keys():
              for v in distances[u].keys(): 
                  correct_dist = distances[u][v] - self.p[u] + self.p[v]
                  if correct_dist < self.min_dist and u != v: self.min_dist = correct_dist
                  correct_distances[u][v] = correct_dist
          return correct_distances

      def main(self):
          self.run_bf()
          if self.p == None: 
              print "Detected negative cycle"
              self.min_dist = None
              return None
          else:
              reweighted_edges = self.create_reweighted_edges()
              d = Dijkstra(self.vertices, self.tail_edges, self.target_edges, reweighted_edges)
              distances_from_s = {}
              for v in self.vertices:
                  distances_from_s[v] = d.main(v)
              self.calculate_correct_distances(distances_from_s)
              return self.min_dist
          
           
           
class TestTests(unittest.TestCase):
    
    def setUp(self):
        pass   
    
    def test_bellmanford_vanilla(self):
        lines = "5 6\n1 2 2\n1 3 4\n2 3 1\n2 4 2\n3 5 4\n4 5 4".split("\n")
        bf = BellmanFord.from_lines(lines)
        self.assertTrue(bf.main(1)[5]==7)
    
    def test_johnson_vanilla(self):
        lines = "6 7\n1 2 -2\n2 3 -1\n3 1 4\n3 5 -3\n3 4 2\n6 5 -4\n6 4 1".split("\n")
        j = Johnson(lines)
        j.run_bf()
        self.assertTrue(j.p[5] ==-6)
        self.assertTrue(j.create_reweighted_edges()=={(1, 2): 0, (6, 4): 2, (3, 1): 1, (2, 3): 0, (3, 4): 0, (6, 5): 2, (3, 5): 0})
        j.main()
        self.assertTrue(j.min_dist==-6)

    def test_johnson_second(self):
        lines = "4 6\n1 2 2\n2 3 4\n3 4 8\n4 1 16\n2 4 -1\n4 2 8".split("\n")
        j = Johnson(lines)
        j.main()
        self.assertTrue(j.min_dist==-1)

    def test_johnson_isolated_vertex(self):
        lines = "5 7\n1 2 2\n2 3 4\n3 4 8\n4 1 16\n2 4 -1\n4 2 8\n5 5 0".split("\n")
        j = Johnson(lines)
        j.main()
        self.assertTrue(j.min_dist==-1)
        #Exclude non-paths from calculation of min
        lines = "5 7\n1 2 2\n2 3 4\n3 4 8\n4 1 16\n2 4 1\n4 2 8\n5 5 0".split("\n")
        j = Johnson(lines)
        j.main()
        self.assertTrue(j.min_dist==1)
    
    def test_johnson_negative_cycle(self):        
        lines = "5 7\n1 2 2\n2 3 4\n3 4 8\n4 1 16\n2 4 1\n4 2 8\n5 5 0\n2 1 -3".split("\n")
        j = Johnson(lines)
        j = Johnson(lines)
        j.main()
        self.assertTrue(j.min_dist==None)




if __name__ == '__main__':
	try:
		lines = file(sys.argv[1],"r")
	except IOError:
		sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
		sys.exit(1)
	J = Johnson(lines.readlines())
        print J.main() 

"""
if __name__ == '__main__':
   unittest.main()
#"""
