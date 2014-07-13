import re, sys, operator
from collections import defaultdict
import heapq
import itertools
from heapq import *



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

class Prim(object):


    def __init__(self, lines):
        self.vertices = set([])
        self.edge_distance = {}
        self.edges = defaultdict(list)
        for line in lines:
            numbers = [int(x) for x in re.findall('-?[0-9]+', line)]
            x = int(numbers[0])
            y = int(numbers[1])
            d = int(numbers[2])
            self.vertices.add(x)#Add source to vertices
            self.vertices.add(y)
            if self.edge_distance.has_key((x,y))==False:
                self.edge_distance[(x,y)] = d
                self.edge_distance[(y,x)] = d
            elif self.edge_distance[(x,y)] > d:
                self.edge_distance[(x,y)] = d
                self.edge_distance[(y,x)] = d
            self.edges[x].append(y)
            self.edges[y].append(x)
        self.vertices = list(self.vertices)
	self.cheap_edge = {}
        self.heap = Priority_Queue()    
        
        

    def calculate_heap(self):
        for terminal in [terminal for terminal in self.vertices if terminal not in self.x]:
            if sum(map(lambda a: self.x.count(a) > 0, self.edges[terminal])) > 0:
                val, vertex = min([(self.edge_distance[(vertex, terminal)], vertex) for vertex in self.edges[terminal] if self.x.count(vertex) > 0])
                self.cheap_edge[terminal] = vertex
            else:
                val = INF
            self.heap.add_task(terminal, val)
          
        
    def add_v(self, v): 
        self.x.append(v)
        self.vertices.remove(v)
        
        


    def main(self):
        s = self.vertices.pop()
        self.x = [s]
        t = 0
        while len(self.vertices) > 0:
            self.calculate_heap()
            
            w, dist = self.heap.pop_task()
            v = self.cheap_edge[w]
            
            t += dist
            self.add_v(w)
        return t



if __name__ == '__main__':
    try:
        gtext = file(sys.argv[1], 'r')
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    glines = gtext.readlines()[1:]
    p = Prim(glines)
    print p.main()     
