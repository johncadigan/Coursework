import sys
import re

class Features():
	
	def __init__(self):
		self.v = {} # Weighted feature fectors
	
	def read_vfile(self, vfile):
		for line in vfile.readlines():
			feature, weight = line.split(' ')
			self.v[feature] = float(weight)
	
	###Feature Functions
	def trigram_tag_feature(self, history, ptag):
		taga, tagb, word, pos = history
		return "TRIGRAM:{0}:{1}:{2}".format(taga, tagb, ptag)
	
	def word_tag_feature(self, history, ptag):
		taga, tagb, word, pos = history
		return "TAG:{0}:{1}".format(word,ptag)
		
	
	def prefix_feature(self, history, ptag):
		taga, tagb, word, pos = history
		return "PREFIX:{0}:{1}".format(word[:3],ptag)
	
	def suffix_feature(self, history, ptag):
		taga, tagb, word, pos = history
		return "SUFFIX:{0}:{1}".format(word[-3::],ptag)

	
	def wordshape_feature(self, history, ptag):
		wordshape = ''
		taga, tagb, word, pos = history
		for x in xrange(0, len(word)):
			if word[x].isupper()==True:
				nxt_shape = 'X'
			elif word[x].islower()==True:
				nxt_shape = 'x'
			elif word[x].isdigit() == True:
				nxt_shape = 'd'
			elif word[x].isdigit() == False and word[x].isalpha() == False:
				nxt_shape = '-'
			if len(wordshape) <= 1:
				wordshape += nxt_shape
			elif len(wordshape) >= 2:
				if  wordshape[-2] != wordshape[-1] != nxt_shape:
					wordshape += nxt_shape
				elif wordshape[-1] != nxt_shape: #or wordshape[-2] != wordshape[-1]:
					wordshape += nxt_shape
		return "WORDSHAPE:{0}:{1}".format(wordshape, ptag)
	
	###
	def compute_sentence_feature_vector(self, sentence, tags):
		
		tags = ['*', '*'] + tags + ['STOP']
		feature_vectors = []
		for k in range(2, len(tags)-1):
			history = (tags[k-2], tags[k-1], sentence[k-2], k) 
			feature_vectors.append(self.compute_feature_vector(history, tags[k]))
		cumulative_vector = {}
		for feature_vector in feature_vectors:
			for feature in feature_vector.keys():
				cumulative_vector.setdefault(feature, 0.0)
				cumulative_vector[feature] += 1.0
		return cumulative_vector
	
	
	
	
	### Compute features
	def compute_feature_vector(self, history, ptag):
		features = []
		features.append(self.trigram_tag_feature(history,ptag))
		features.append(self.word_tag_feature(history,ptag))
		features.append(self.suffix_feature(history,ptag))
		features.append(self.prefix_feature(history,ptag))
		features.append(self.wordshape_feature(history,ptag))
		feature_vector = {}
		for feature in features:
			feature_vector[feature] = 1.0
			
		return feature_vector
	
	
	def VxG(self, history, ptag): #Multiplies the weights (V) and feature vector (G)
		g = self.compute_feature_vector(history, ptag)
		total = 0.0
		for x in g.keys():
			if self.v.has_key(x):
				total += self.v[x] * g[x]
		return total
	
	def adjust_v(self, golden_vector, res_vector):
		for key in golden_vector.keys():
			self.v[key] += golden_vector[key]
		for key in res_vector.keys():
			self.v.setdefault(key, 0.0)
			self.v[key] -= res_vector[key]



class GLM_NER():
	
	def __init__(self, training_file, iterations, vfile):
		self.features = Features()
		self.lines = training_file.readlines()
		self.results = []
		if vfile:
			self.features.read_vfile(vfile)
		
	
	
	def train(self, iterations):
		iteration = 0
		sentences = []
		sentence = []
		golden_data = []
		golden_tags = []
		
		for line in self.lines[:-1]:
			if line != '\n':
				word, tag = line.split(' ')
				sentence.append(word.strip())
				golden_tags.append(tag.strip())
			else:
				sentences.append(sentence)
				golden_data.append(golden_tags)
				if len(sentence) != len(golden_tags):
					print "tags don't match words"
				sentence = []
				golden_tags = []
		
		#Initialize weighted vector existing features
		tags = list(set(golden_tags))
		for x in range(0, len(sentences)):
			sentence = sentences[x]
			tags = golden_data[x]
			self.features.v.update(self.features.compute_sentence_feature_vector(sentence, tags))# Results from product are tuples, but they need to be lists
		for key in self.features.v.keys():
			self.features.v[key] = 0.0
		
		while iteration < iterations:
			print "Iteration {0}\n".format(iteration+1)
			for x in range(0, len(sentences)):
				#print x, ' ', sentences[x]
				sentence = sentences[x]
				words, res_tags = self.viterbi(sentence)
				res_vector = self.features.compute_sentence_feature_vector(words, res_tags)
				if res_tags != golden_data[x]:
					golden_vector = self.features.compute_sentence_feature_vector(words, golden_data[x])
					self.features.adjust_v(golden_vector, res_vector)
			iteration+=1
		
		f = open('trained_v', 'wb')
		for key in self.features.v.keys():
			f.write('{0} {1}\n'.format(key, self.features.v[key]))
		f.close()
				
			
	def viterbi(self, sentence):
		
		tags = []
		pi = {(-1,'*','*'): 1} #The probability of tags up to this point in the hidden markov model; name from pseudo code
		s = {-2: '*',-1 : ['*']} #The possible states by position; the second one is a list to make the function work below 
		back_pointer = {}
		max_result = {}
		y = {} # y contains the final decision for each position
		for number in xrange(0, len(sentence)):
			s[number] = ['I-GENE', 'O']# Give each word in the sentence its possible states
		for k in xrange(0, len(sentence)):
			x = sentence[k] #x is the word at position k
			for v in s[k-1]: # Order of possible states contributing to the calculation: u v w
				for w in s[k]: 
					score, tag = max([(pi[(k-1, u, v)] + self.features.VxG((u,v,x,k), w), u) for u in s[k-2]]) #Gets the most likely tag and its score based on all prior scores of bigram tags and the probability of the individual tag based on the word
					pi[(k,v,w)] = score
					back_pointer[(k,v,w)] = tag

		if len(sentence) > 1:
			score, vtag, wtag = max([(pi[(len(sentence)-1, v, w)] + self.features.VxG((v,w,x,k),'STOP'), v, w) for v in ['I-GENE', 'O'] for w in ['I-GENE', 'O']]) #Final prob
		else:
			k = len(sentence)
			score, tag= max([(pi[(k-2, '*', '*')] + self.features.VxG((u,v,sentence[k-1],k), u), u) for u in s[k-1]])
			return (sentence, [tag])
		pi[(len(sentence),wtag,'STOP')] = score 
		back_pointer[(len(sentence),w,'STOP')] = wtag #Back pointer's final tag
		y[len(sentence)-2] = vtag #Penultimate tag
		y[len(sentence)-1] = wtag #Final tag
		


		for k in xrange(len(sentence)-3, -1, -1): #Iterate backwards through the backpointer
			y[k] = back_pointer[(k+2,y[k+1],y[k+2])] #Finds the tag based on the two which follow it in the back pointer
		for x in xrange(0, len(sentence)): #Print out word tag pairs starting at the beginning of the sentence
			tags.append(y[x])
			
#		print sentence[x] + ' ' + y[x]
		return (sentence, tags)

	def tag(self, lines):
		sentences = []
		sentence = []
		
		for line in lines:
			word = line.strip()
			if len(word) > 0: sentence.append(word)
			elif len(word) == 0:
				sentences.append(sentence)
				sentence = []
		
		for sentence in sentences:
			sentence, tags = self.viterbi(sentence)
			for x in range(0, len(sentence)):
				self.results.append("{0} {1}".format(sentence[x], tags[x]))
			self.results.append(' ')


	
	
	def write_results(self, output):
			for line in self.results:            
				output.write("{0}\n".format(line))

if __name__ == "__main__":
	
	try:
		training_lines = file(sys.argv[1],"r")
		iterations = sys.argv[2]
		test_lines = file(sys.argv[3],"r")
	except IOError:
		sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
		sys.exit(1)

	vfile = raw_input("Please input name of weighted vector file or '' to start from the start")
	if vfile:
		vfile = file(vfile)
		tagger = GLM_NER(training_lines, iterations, vfile)
	else:
		tagger = GLM_NER(training_lines, iterations, vfile=None)
	tagger.train(int(iterations))
	tagger.tag(test_lines)
	ofile = raw_input("Please input name of output file")
	f = file(ofile, 'wb')
	tagger.write_results(f)
