import re, sys, random

class KargerMCG:

	def __init__(self, lines):
		# for example cases
		self.vertices = []
		self.edges = [] #Edges are tuples with the name of each vertex
		#For faster computations
		self.vertex_pointer = {} #Gives a list of all connected vertices given one vertex
		self.edge_pointer = {} #Gives the two vertices for every edge
		for line in lines:
			numbers = [int(x) for x in re.findall('[0-9]+', line)] #Find all numbers in a line; The line 1 2 3 means that there are edges (1,2) and (1,3)
			self.vertices.append(int(numbers[0]))
			self.vertex_pointer[numbers[0]] = numbers[1:]
			for number in numbers[1:]:
				self.vertex_pointer[numbers[0]] = numbers[1:]
				new_edge, pointers = self.make_edge(numbers[0], number)
				self.edge_pointer[new_edge] = pointers
				self.edges.append(new_edge)
		self.edges = set(self.edges)
		print 'vertices', len(self.vertices), 'edges', len(self.edges)
	
	def make_edge(self, vertex_x, vertex_y): #Edges are recorded as a tuple (Lower number, Greater number)
		pointers = [vertex_x, vertex_y]
		returned_edge = None
		if vertex_x > vertex_y:
			returned_edge = tuple((vertex_y, vertex_x))
		elif vertex_x < vertex_y:
			returned_edge = tuple((vertex_x, vertex_y))
		if returned_edge == None: print 'ERROR', vertex_x, vertex_y #Error checking
		return returned_edge, pointers
			
	def main(self, iterations): #Runs through number of iterations and returns the minimum
		i = iterations
		min_cut = None
		while i > 0:
			vertices = list(self.vertices)
			edges = list(self.edges)
			cut = self.karger_cut(vertices, edges)
			i = i - 1
			if min_cut == None or cut < min_cut: min_cut = cut
		print min_cut
	
	
	def karger_cut(self, vertices, edges):
		v_pointer = self.vertex_pointer.copy()
		e_pointer = self.edge_pointer.copy()
		supernodes = []
		while len(vertices) > 2: #Keep combining nodes until 2 are left
			remove_edge = random.choice(edges)#Choose a random edge
			vers = e_pointer[remove_edge]#Get the two nodes from edge
			for x in range(0, edges.count(remove_edge)):
				edges.remove(remove_edge)
			x, y = vers
			new_edges = []#To store the recalculated edges
			vertices.remove(y)#Remove an edge
			supernodes.append(tuple((y, x)))#Note the combination of x and y
			for edge in edges:#Iterate through edges
				a, b = edge
				if a == y and b!=x:#If a was the removed edge
					new_edge, pointers = self.make_edge(x, b)#Make b the nexus for y's edges
				elif b == y and a!=x: #If b was the removed edge
					new_edge, pointers = self.make_edge(a, x)#Make a the nexus for y's edges
				elif a!=b: new_edge, pointers = (a, b), [a,b]#If it was not altered; keep it the same
				e_pointer[new_edge] = pointers#Update the pointers for the edges
				new_edges.append(new_edge)
				edges = new_edges #Update edges
		return len(edges)
			   

if __name__ == '__main__':
	
	try:
		adj_list = file(sys.argv[1],"r")
	except IOError:
		sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
		sys.exit(1)
	MinCut = KargerMCG(adj_list.readlines())
	iterations = int(raw_input("Please input the number of iterations"))
	MinCut.main(iterations)
	
