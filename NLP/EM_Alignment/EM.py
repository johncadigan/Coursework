import sys
from collections import defaultdict
from math import log
import re
import codecs
import abc
import json
	
class ParallelCorpus():
	# often English
	TargetArray = []
	# the "foreign" language
	SourceArray = []
	index = 0
	
	@staticmethod
	def read_file_to_array(file, array):
		infile = file.readlines()
		for line in infile:
			array.append(line)
		pass
	
	def size(self):
		return len(self.TargetArray)
		pass
	
	def __init__(self, source_file, target_file):
		self.read_file_to_array(target_file, self.TargetArray)
		self.read_file_to_array(source_file, self.SourceArray)
		TargetSize = len(self.TargetArray)
		SourceSize = len(self.SourceArray)
		
		if TargetSize != SourceSize: 
			raise ValueError("The corpora must have the same size. English: %d, Spanish: %d", TargetSize, SourceSize)        
		pass
	
	def __iter__(self):
		return self
	
	def next(self, index):
		if self.index == len(self.SourceArray):
			raise StopIteration
		result = (self.SourceArray[index], self.TargetArray[index])
		return result
	
	def sentences(self, index):
		SSentence, TSentence = self.SourceArray[index].split(), self.TargetArray[index].split()
		return (SSentence, TSentence)
	
	def reset(self):
		self.index = 0
	pass
	
class EM(): #Provided
	
	@ abc.abstractmethod
	def delta(self, (i,j,k)):
		return                   
	
	@ abc.abstractmethod
	def get_t(self, f_k, e_k):
		return
			
	def get_c(self, num, key):
		if self.c[num].has_key(key):
			return self.c[num][key]
		else: return 0.0 
	
	@ abc.abstractmethod    
	def afteriteration(self, iteration):
		return
	
	@ abc.abstractmethod
	def train(self, iterations):
		return
	
	@ abc.abstractmethod
	def align(self, source_file, targer_file):
		return
	
	def write_results(self, output):
			"""
			Writes results to the output file object.
			Format:
	
			"""
			# First write counts for emissions
			for line in self.results:            
				output.write("%s\n" % (line))    
	
class EM1(EM):
	
	def __init__(self, training_source_file, training_target_file):
		self.t = {}
		self.c = {1: {}, 2: {}, 3: {}, 4: {}} #Counts in each iteration; name from pseudo code
		self.PCorpus = ParallelCorpus(training_source_file, training_target_file)
		self.results = []
	
	def get_t(self, f_k, e_k): #
		f_k = unicode(f_k)
		e_k = unicode(e_k)
		if self.t[e_k].has_key(f_k):
			return self.t[e_k][f_k]
		else: return 0.0
		
	def init_t(self): 
		f = open('first_t_values', "w+")
		pre_t = {}
		for k in xrange(0, self.PCorpus.size()): #Iterate over the entire corpus
				SSentence, TSentence = self.PCorpus.sentences(k)
				TSentence.insert(0, 'NULL') #Adds the possibility that a source word translates to NULL
				l = len(SSentence)
				m = len(TSentence)
				for i in xrange(0, l):
					for j in xrange(0, m):
						s_k = unicode(SSentence[i])
						t_k = unicode(TSentence[j])
						pre_t.setdefault(t_k,set([]))
						pre_t[t_k].add(s_k) #Adds all possible translations of an source word, including to null in sentence k
		for t_word in pre_t.keys():
			for s_word in pre_t[t_word]:
				denom = float(len(pre_t[t_word])) 
				score = float(1)/denom
				self.t.setdefault(t_word, {})
				self.t[t_word][s_word] = score #The emission of a target word from a source word is initialized to be equiprobable; there is also the chance that the source word translates to NULL
				f.write('{0} {1} {2}\n'.format(s_word, t_word, self.t[t_word][s_word]))
		f.close()
		
	def delta(self, tupe):
		i,j,k = tupe
		SSentence, TSentence = self.PCorpus.sentences(k)
		TSentence.insert(0, "NULL")
		n_s_k = unicode(SSentence[i])
		n_t_k = unicode(TSentence[j])
		l = len(TSentence)
		denom = 0.0
		for index in range(0,l): #Adds up the counts of all possible translations, including to NULL
			t_k = unicode(TSentence[index])
			denom += self.get_t(n_s_k,t_k)
		score = self.get_t(n_s_k,n_t_k)/float(denom) #Delta equals the probability of a given alligment out of all possible alignments of a sentence; The sum of all deltas for a sentence is one
		return score
		
	def train(self, iterations):
		self.init_t()#Makes all translations equiprobable
		print 'EM1 initialized'
		iteration = 0
		#f = file('c_values', 'w+')
		while iteration < iterations:
			self.c = {1: {}, 2: {}} #to reform counts with delta
			for k in xrange(0, self.PCorpus.size()):
				SSentence, TSentence = self.PCorpus.sentences(k)
				TSentence.insert(0, 'NULL')
				l = len(SSentence)
				m = len(TSentence)
				for i in xrange(0, len(SSentence)):
					for j in xrange(0, len(TSentence)):
						d = self.delta((i,j,k)) #The amount by which to change the probability of a given alignment
						s_k = unicode(SSentence[i])
						t_k = unicode(TSentence[j])
						self.c[1].setdefault((s_k, t_k), 0.0) #counts are initialized at 0 and modified
						self.c[2].setdefault((t_k), 0.0)
						self.c[1][(s_k, t_k)] = self.c[1][(s_k, t_k)] + d # Joint count is incremented
						self.c[2][(t_k)] = self.c[2][(t_k)] + d #Overall count is incremented
						#f.write('{0} {1} {2} {3} {4}\n'.format(self.get_c(1, (s_k, t_k)), self.get_c(2, (t_k)), d, t_k, s_k))
			self.after_iteration() #Recalculate t values           
			iteration += 1
			print 'iteration', str(iteration)
		self.write_t() #Write t values
	
	def write_t(self): #Writes the t values
		f = open('t_values', "w+")
		for e_k in self.t.keys():
			for f_k in self.t[e_k].keys():
				f.write('{0} {1} {2}\n'.format(unicode(f_k), unicode(e_k), self.t[e_k][f_k]))
		f.close()
		
	
	def after_iteration(self): #Recalculates t value based on new counts
		for t_k in self.t.keys():
			for s_k in self.t[t_k].keys():
				s_k = unicode(s_k)
				t_k = unicode(t_k)
				self.t[t_k][s_k] = float(self.c[1][(s_k, t_k)])/float(self.c[2][(t_k)])
	
	def align(self, translate_source_file, translate_target_file):
		f = open('em1.dev.out', "w+")
		s_sentences = translate_source_file.readlines()
		t_sentences = translate_target_file.readlines()
		c = str(s_sentences)
		for k in xrange(0, len(s_sentences)):
				SSentence, TSentence = s_sentences[k].split(), t_sentences[k].split()
				TSentence.insert(0, 'NULL')
				l = len(TSentence)
				m = len(SSentence)
				for i in xrange(0, m):
					s_k = unicode(SSentence[i])
					score, index = max([(self.get_t(s_k, unicode(TSentence[j])), j) for j in range(0, l)])
					if index != 0:
						f.write("{0} {1} {2}\n".format(k+1, index, i+1)) #Writes alignment of word from corpus
		f.close()
		self.write_t()
		
class EM2(EM):
	
	def __init__(self, training_source_file, training_target_file):
		self.PCorpus = ParallelCorpus(training_source_file, training_target_file)
		self.t = {}
		self.c = {1: {}, 2: {}, 3: {}, 4: {}}
		self.results = []
		self.q = {}
	
	def init_q(self): #All q values start as equiprobable (Allignment of source position (i) to target position (j) for a sentence of length l+1 (one more for NULL)
		for k in xrange(0, self.PCorpus.size()):
				SSentence, TSentence = self.PCorpus.sentences(k)
				TSentence.insert(0, 'NULL')
				m = len(SSentence)
				l = len(TSentence)
				for i in xrange(0, m):
					for j in xrange(0, l):
						self.q[(j,i,l,m)] = 1.0/(1.0+l) #one more for null
	
	def get_t(self, s_k, t_k): #Same as before
		s_k = unicode(s_k)
		t_k = unicode(t_k)
		if self.t[t_k].has_key(s_k):
			return self.t[t_k][s_k]
		else: return 0.0
	
	def get_q(self, (j,i,l,m)): #Returns q if it exists
		if self.q.has_key((j,i,l,m)):
			return self.q[(j,i,l,m)]
		else: return 0.0
		
	def t_read(self, t_file): #Reads t file to set t values
		f = codecs.open(t_file, "r", "utf-8")
		lines = f.readlines()
		for line in lines:
			s_word, t_word, score = line.split()
			score = score.strip()
			self.t.setdefault(t_word, {})
			self.t[t_word][s_word] = float(score)
	
	def delta(self, (i,j,k)):# Calculates delta with all possibilities of both t (word alignment) and q (position alignment)
		SSentence, TSentence = self.PCorpus.sentences(k)
		TSentence.insert(0, 'NULL')
		n_f_k = unicode(SSentence[i])
		n_e_k = unicode(TSentence[j])
		m = len(SSentence)
		l = len(TSentence)
		denom = 0.0
		for index in range(0,l):#Denominator is the sum of all possible alignments
			e_k = unicode(TSentence[index])
			denom += self.get_t(n_f_k,e_k)*self.get_q((index,i,l,m))
		score = (self.get_t(n_f_k,n_e_k)*self.get_q((j,i,l,m)))/float(denom)
		return score
	
	def train(self, iterations, t_file):
		self.t_read(t_file) 
		self.init_q()
		print 'EM2 initialized'
		iteration = 0
		#f = file('c_values', 'w+') #From debugging
		while iteration < iterations:
			self.c = {1: {}, 2: {}, 3: {}, 4: {}}#re-initialize counts
			for k in xrange(0, self.PCorpus.size()):
				SSentence, TSentence = self.PCorpus.sentences(k)
				TSentence.insert(0, 'NULL')
				m = len(SSentence)
				l = len(TSentence)
				for i in xrange(0, m):
					for j in xrange(0, l):
						d = self.delta((i,j,k))# Amount by which to modify counts
						f_k = unicode(SSentence[i])
						e_k = unicode(TSentence[j])
						#Set all counts for each possibility to 0
						self.c[1].setdefault((f_k, e_k), 0.0)
						self.c[2].setdefault((e_k), 0.0)
						self.c[3].setdefault((j,i,l,m), 0.0)
						self.c[4].setdefault((i,l,m), 0.0)
						#Counts for both t (1,2) and q (3,4) grow by a portion of 1 (d = delta)
						self.c[1][(f_k, e_k)] = self.c[1][(f_k, e_k)] + d
						self.c[2][(e_k)] = self.c[2][(e_k)] + d
						self.c[3][(j,i,l,m)] = self.c[3][(j,i,l,m)] + d
						self.c[4][(i,l,m)] = self.c[4][(i,l,m)] + d
			#f.write('{0} {1} {2}\n'.format(self.q[(3,2,8,8)], '->', self.c[3][(3,2,8,8)]/self.c[4][(2,8,8)])) #For debugging
			self.after_iteration() #Recalculate t and q based on counts
			iteration += 1
			print 'iteration', str(iteration)
	
	def after_iteration(self):
		for e_k in self.t.keys():
			for f_k in self.t[e_k].keys():
				self.t[e_k][f_k] = float(self.c[1][(f_k,e_k)])/float(self.c[2][(e_k)])
		for key in self.q.keys():
			j,i,l,m = key
			self.q[key] = float(self.c[3][key])/float(self.c[4][(i,l,m)])
	
	def align(self, translate_source_file, translate_target_file):
		f = open('em2.dev.out', "w+")
		s_sentences = translate_source_file.readlines()
		t_sentences = translate_target_file.readlines()
		for k in xrange(0, len(s_sentences)):
				SSentence, TSentence = s_sentences[k].split(), t_sentences[k].split()
				TSentence.insert(0, 'NULL')
				l = len(TSentence)
				m = len(SSentence)
				for i in xrange(0, m):
					f_k = unicode(SSentence[i])
					score, index = max([(self.get_t(f_k,TSentence[j])*self.get_q((j,i,l,m)), j) for j in range(0, l)])
					if index != 0:
						f.write("{0} {1} {2}\n".format(k+1, index, i+1))
		f.close()
	
if __name__ == "__main__":
	
	
	try:
		training_source_file = codecs.open(sys.argv[1], 'r+', 'utf-8')
		training_target_file = codecs.open(sys.argv[2], 'r+', 'utf-8')
		translate_source_file = codecs.open(sys.argv[3], 'r+', 'utf-8')
		translate_target_file = codecs.open(sys.argv[4], 'r+', 'utf-8')
	except IOError:
		sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
		sys.exit(1)
	
	# Initialize EM
	reload(sys)
	sys.setdefaultencoding("utf-8")
	#FTranslator = EM1(training_source_file, training_target_file)
	#FTranslator.train(5)
	#FTranslator.align(translate_source_file, translate_target_file)
	iterations = int(raw_input("Please input the desired number of training iterations"))
	STranslator = EM2(training_source_file, training_target_file)    
	STranslator.train(iterations, 't_values') #Training starts with t values made with EM1
	STranslator.align(translate_source_file, translate_target_file)
	
