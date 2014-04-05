import sys

class Count_QS:

	def __init__(self, array):
		self.comps = 0
		self.results = [0] * len(array)
		
	#Quicksort pivot chosen from first number
	def first_qs(self, numlist):
		pivot = numlist[0]
		qslist = self.quicksort(numlist, pivot)
		self.results[self.results.index(0)+qslist.index(pivot)] = pivot #Put the pivot in the right spot
		if len(qslist[:qslist.index(pivot)+1]) > 1: # Sort the lower array recursively
			self.first_qs(qslist[:qslist.index(pivot)])
		if len(qslist[qslist.index(pivot)+1:]) > 0: # Sort the greater array recursively
			self.first_qs(qslist[qslist.index(pivot)+1:])
		
		
	#Quicksort pivot chosen from last number
	def final_qs(self, numlist):
		pivot = numlist[-1]
		numlist[0], numlist[-1] =  pivot, numlist[0] #Put the final number at the first position, so quicksort works as normal
		qslist = self.quicksort(numlist, pivot)
		self.results[self.results.index(0)+qslist.index(pivot)] = pivot #Put the pivot in the right spot
		if len(qslist[:qslist.index(pivot)+1]) > 1: # Sort the lower array recursively
			self.final_qs(qslist[:qslist.index(pivot)])
		if len(qslist[qslist.index(pivot)+1:]) > 0: # Sort the greater array recursively
			self.final_qs(qslist[qslist.index(pivot)+1:])
	
	#Quicksort pivot chosen as median of firat, last and middle numbers
	def median_qs(self, numlist):
		pivot = numlist[0] #For arrays of length 1 and 2, default to having the pivot as the first number
		if len(numlist) >= 3:
			first = numlist[0]
			final = numlist[-1]
			if len(numlist) & 1: #Odd length
				middle = numlist[((len(numlist)+1)/2)-1]
			else: #Even
				middle = numlist[(len(numlist)/2)-1]
			three = [first, middle, final]
			three.sort()
			pivot = three[1]
		pivot_index = numlist.index(pivot)
		numlist[0], numlist[pivot_index] =  pivot, numlist[0]#Put pivot at first position to run with standard quicksort
		qslist = self.quicksort(numlist, pivot)
		self.results[self.results.index(0)+qslist.index(pivot)] = pivot #Put the pivot in its absolute position
		if len(qslist[:qslist.index(pivot)+1]) > 1: # Sort the lower array recursively
			self.median_qs(qslist[:qslist.index(pivot)])
		if len(qslist[qslist.index(pivot)+1:]) > 0: # Sort the greater array recursively
			self.median_qs(qslist[qslist.index(pivot)+1:])
		
	#Standard quicksort
	def quicksort(self, numlist, pivot): #Re-orders a list around a pivot
		l=0
		i = 1#The future position of the pivot
		if len(numlist) == 1: return numlist
		self.comps += len(numlist)-1 #Add a computation for every comparison
		for j in xrange(l, len(numlist)):
			if numlist[j] < pivot:#For numbers smaller thant he pivot
				numlist[j], numlist[i] = numlist[i], numlist[j] #Set them less than the future position of the pivot
				i += 1#Increment future position of the pivot by 1
		numlist[l], numlist[i-1] = numlist[i-1], numlist[l] #Put the pivot ahead of the numbers it is greater than
		return numlist

if __name__ == '__main__':
	
	try:
		array_file = file(sys.argv[1],"r")
	except IOError:
		sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
		sys.exit(1)
	array = []
	for line in array_file.readlines():
		line = line.strip()
		if line.isdigit():
			array.append(int(line.strip()))
	First = Count_QS(array)
	Final = Count_QS(array)
	Median = Count_QS(array)
	First.first_qs(list(array))# Make sure each one runs on a different list object
	print "Quicksort by first number: {0} computations".format(First.comps)
	Final.final_qs(list(array))
	print "Quicksort by first number: {0} computations".format(Final.comps)
	Median.median_qs(list(array))
	print "Quicksort by median of first, middle and final numbers: {0} computations".format(Median.comps)
	

            
