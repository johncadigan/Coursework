import re
import random
from collections import Counter, defaultdict
import operator
import sys
sys.setrecursionlimit(1000000)
filename = sys.argv[-1]
f = file(filename, 'r+')
lines = f.readlines()

class Strong_Graph:

	def __init__(self, lines):
		self.vertices = set([])
		self.explored_vertices = [] #Implemented as stack
		self.edges = defaultdict(list)
		self.start = None
		for line in lines:
			x, y = [int(x) for x in re.findall('[0-9]+', line)]# Numeric
			#x, y = [x for x in re.findall('[A-Z]+', line)]# Alphabetical
			#Existing edges
			if x == y:
				print "Error! No edge can point to itself!"
			self.edges["v{0}".format(x)].append("v{0}".format(y)) #Forward edges
			self.edges["{0}v".format(y)].append("{0}v".format(x)) #Reverse edges
			self.vertices.add(x)
		

	
	def main(self):
		# reverse order
		print 'starting first'
		self.vertices = list(self.vertices)
		self.vertices.reverse()
		rev_res = []
		for x in self.vertices:
			x = "v{0}".format(x)
			print x
			if rev_res.count(x) == 0:
				print x, self.Iterative_DFS(x, rev_res)
				
		print rev_res
		# second pass
		print 'starting second'
		traversed = []
		prev_length = 0
		SCCs = {}
		while rev_res:
			x = rev_res.pop()
			numbers = re.findall('([0-9]+)', x)
			start = "{0}{1}".format('v', numbers[0])
			print start
			if traversed.count(start) == 0:
				#print "Input", start, 'explored', traversed
				res = self.Iterative_DFS(start, traversed)
				print res, len(res), len(traversed)
				SCCs[start] = len(res) - prev_length
				traversed = res
				prev_length = len(res)
				print SCCs
				#print res
		sorted_SCCs = sorted(SCCs.iteritems(), key=operator.itemgetter(1))
		print sorted_SCCs[0:4]
		#common = Counter(self.leader.values()) 
		#print common.most_common(5)
	
	def DFS_Loop(self, vertices, edges):
		self.t = 0
		self.s = None
		self.finishing_time = {}
		self.leader = {}
		nodes = vertices.keys()
		nodes.reverse()
		for i in nodes:
			if vertices[i] == 0:
				self.s = i
				self.DFS(vertices, edges, i)
	

			    
	def Iterative_DFS(self, start, visited = []):
		stack = [start]
		while stack:
			vertex = stack.pop()
			if vertex not in visited:
				visited.append(vertex)
				to_visit = list(set(self.edges[vertex])-set(visited))
				if len(to_visit) > 0:
					stack.append(to_visit[0])
		return visited
		
		
class Kosaraju():
	
	
	def __init__(self,lines):
		self.vertices = set([])
		self.S = [] #Implemented as stack
		self.G = defaultdict(list)
		for line in lines:
			x, y = [int(x) for x in re.findall('[0-9]+', line)]# Numeric
			#x, y = [x for x in re.findall('[A-Z]+', line)]# Alphabetical
			#Existing edges
			if x == y:
				print "Error! No edge can point to itself!"
			else:
				self.G["v{0}".format(x)].append("v{0}".format(y)) #Forward edges
				self.G["{0}v".format(y)].append("{0}v".format(x)) #Reverse edges
			self.vertices.add(x)
			
	def Iterative_DFS1(self, start, visited=[]):
		finished = []
		stack = [start]
		while stack:
			vertex = stack[-1]
			if vertex not in visited:
				visited.append(vertex)
				to_visit = list(set(self.G[vertex])-set(visited))
				if len(to_visit) > 0:
					stack.extend(to_visit)
			else:
				if finished.count(vertex) == 0:
					finished.insert(0, vertex)
			stack.pop()
		return finished
	
	def Iterative_DFS2(self, start, visited = []):
		stack = [start]
		while stack:
			vertex = stack.pop()
			if vertex not in visited:
				visited.append(vertex)
				to_visit = list(set(self.G[vertex])-set(visited))
				if len(to_visit) > 0:
					stack.append(to_visit[0])
		return visited
	
	def main(self):
		self.vertices = list(self.vertices)
		self.vertices.reverse()
		for x in self.vertices:
			x = "v{0}".format(x)
			if self.S.count(x) == 0:
				print x, self.Iterative_DFS1(x,self.S) 
		print 'starting second'
		traversed = []
		prev_length = 0
		SCCs = {}
		print self.S, rev
		while rev:
			x = rev.pop(0)
			numbers = re.findall('([0-9]+)', x)
			start = "{0}{1}".format('v', numbers[0])
			if traversed.count(start) == 0:
				res = self.Iterative_DFS2(start, traversed)
				SCCs[start] = len(res) - prev_length
				traversed = res
				prev_length = len(res)
		sorted_SCCs = sorted(SCCs.iteritems(), key=operator.itemgetter(1), reverse=True)
		print sorted_SCCs[0:5]
		
lines = ['1 2', '2 3', '2 4', '2 5', '3 6', '4 5', '4 7', '5 2', '5 6', '5 7', '6 3', '6 8', '7 8', '7 10', '8 7', '9 7', '10 9', '10 11', '11 12', '12 10']
#lines = ['A B', 'A C', 'C D', 'C E', 'B D', 'B E', 'E A', 'D E']
j = Kosaraju(lines)
#j.edges ={'A':['B','C'],'B':['D','E'],'C':['D','E'],'D':['E'],'E':['A']}
j.main()
