#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, operator
from collections import defaultdict
import heapq
import itertools
from heapq import *
from datetime import *

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
		


class Dijkstra:

	def __init__(self, lines):
		
		self.vertices = set([])
		self.edge_distance = {}
		self.edges = defaultdict(list)
		for line in lines:
			numbers = [int(x) for x in re.findall('[0-9]+', line)]
			x = numbers[0]
			self.vertices.add(x)#Add source to vertices
			for indx in xrange(2, len(numbers), 2):#Read of each destination, length pair
				y = numbers[indx-1]
				l = numbers[indx]
				self.edge_distance[(x,y)] = l
				self.edges[x].append(y)
		self.vertices = list(self.vertices)
		self.vertices.sort()
	
	def find_min(self, dists, vertices):
		for x in sorted(dists.iteritems(), key=operator.itemgetter(1)):
			x, number = x
			if x in vertices:
				return x
	
	
	def slow_dijkstras(self, initial=None):
		if initial == None: initial = self.vertices[0]
		dist = {}
		vertices = list(self.vertices) #A separate copy
		for v in vertices: #Default dist to inf
			dist[v] = INF
		dist[initial] = 0 #Source is set to 0
		while vertices:
			points = float('inf')
			u = self.find_min(dist, vertices)
			vertices.remove(u)
			if dist[u] == INF:#Should not run
				break
			for v in self.edges[u]:
				alt = dist[u] + self.edge_distance[(u,v)]
				if alt < dist[v]:
					dist[v] = alt
		return dist
	

	
	def fast_dijkstras(self, initial= None):
		if initial == None: initial = self.vertices[0]
		PQ = Priority_Queue()
		dist = {}
		for v in self.vertices: #Default dist to inf
			dist[v] = INF
			PQ.add_task(v, priority = INF)
		dist[initial] = 0
		while len(PQ) > 0:
			u = PQ.pop_task()
			u, priority = u
			for v in self.edges[u]:
				alt = dist[u] + self.edge_distance[(u,v)]
				if alt < dist[v]:
					dist[v] = alt
					PQ.add_task(v, priority = alt)
		return dist
		
					
			
	
	def main(self, endpoints):#Endpoints can either be of the form (destination, key) or destination
		sstart = datetime.now()
		sdistances = self.slow_dijkstras()
		sstop = datetime.now()
		fstart = datetime.now()
		fdistances = self.fast_dijkstras()
		fstop = datetime.now()
		stime = sstop-sstart
		stime = stime.microseconds/float(1000000) + stime.seconds
		ftime = fstop-fstart
		ftime = ftime.microseconds/float(1000000) + ftime.seconds
		print "Array: {0:.4f} \t Priority Queue: {1:.4f} \t Increase {2:.4f}".format(stime, ftime, stime/ftime) 
		print "Destination \t Key \t Slow results \t Fast results\n" 
		for destination in endpoints:
			tupe = destination
			if type(tupe) != tuple:#If destinations are do not include information
				tupe = (destination, 'N\A')
			destination, score = tupe
			print "{0} \t\t {1} \t\t {2} \t\t {3} \n".format(destination, score, sdistances[destination], fdistances[destination])  
			

if __name__ == '__main__':
	try:
		adj_list = file(sys.argv[1],"r")
	except IOError:
		sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
		sys.exit(1)
	D = Dijkstra(adj_list.readlines())
	D.main([(7, 2599),(37,2610),(59,2947), (82,2052), (99,2367), (115,2399), (133,2029), (165,2442), (188,2505), (197,3068)])
	

