import re
import random
from collections import Counter
import sys
sys.setrecursionlimit(5105050)

filename = sys.argv[-1]
f = file(filename, 'r+')
lines = f.readlines()

class Strong_Graph:

	def __init__(self, lines):
		self.vertices = {}
		self.reverse_edges = {}
		number_mapper = []
		for line in lines:
			numbers = [int(x) for x in re.findall('[0-9]+', line)]
			x = int(numbers[0])
			y = int(numbers[1])
			self.vertices[x] = 0
			self.vertices[y] = 0
			if self.reverse_edges.has_key(x) == False: self.reverse_edges[x] = []
			if self.reverse_edges.has_key(y): self.reverse_edges[y].append(x)
			elif self.reverse_edges.has_key(y) == False: self.reverse_edges[y] = [x]
		print len(self.reverse_edges.values()), len(self.vertices.values())
	
	
	def main(self):
		# reverse order
		print 'starting first'
		vertices = self.vertices
		reverse_edges = self.reverse_edges
		for x in vertices:
			if reverse_edges[x].count(x) > 0: print 'error with', x
		self.DFS_Loop(vertices, reverse_edges)
		# second pass
		print 'starting second'
		self.new_edges = {}
		self.new_vertices = {}
		for vertex in self.vertices.keys():
			x = self.finishing_time[vertex] 
			edges = self.reverse_edges[vertex]
			for edge in edges:
				y = self.finishing_time[edge] 
				self.new_vertices[x] = 0
				self.new_vertices[y] = 0
				if self.new_edges.has_key(x) == False: self.new_edges[x] = []
				if self.new_edges.has_key(y): self.new_edges[y].append(x)
				elif self.new_edges.has_key(y) == False: self.new_edges[y] = [x]
		new_edges = self.new_edges
		new_vertices = self.new_vertices
		del self.reverse_edges
		self.DFS_Loop(new_vertices, new_edges)
		common = Counter(self.leader.values())
		print common.most_common(5)
		
	
	def DFS(self, vertices, edges, i):
		vertices[i] = 1
		self.leader[i] = self.s
		arcs = edges[i]
		for arc in arcs:
			k = arc
			if vertices[k] == 0:
				self.DFS(vertices, edges, k)
		self.t += 1
		self.finishing_time[i] = self.t
		
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

j = Strong_Graph(lines)
j.main()
