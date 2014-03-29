import sys
from collections import defaultdict
from math import log
import re


class HMM_Tagger():

    def __init__(self, training_lines):
        self.emissions = {}
        self.unigrams = {}
        self.bigrams = {}
        self.trigrams = {}
        self.calculated_trigram = {}
        self.results = []
        words = []
        special_tags = ['_RARE_']
        lines = training_lines.readlines()
        for x in special_tags:
            self.emissions[(x, 'O')] = 0
            self.emissions[(x, 'I-GENE')] = 0  
        for line in lines:   
            if line.find('WORDTAG') > 0: #(TAG|Word)
                number, info, tag, word = line.split(' ')
                word = word.strip()
                self.emissions[(word, tag)] = float(number)
            elif line.find('1-GRAM') > 0: #(TAG) counts of each tag
                number, info, tag = line.split(' ')
                tag = tag.strip()
                self.unigrams[tag] = float(number)
            elif line.find('2-GRAM') > 0: #(TAG1 TAG2) counts of each tag bigram
                number, info, tagone, tagtwo = line.split(' ')
                self.bigrams[(tagone.strip(), tagtwo.strip())] = float(number)
            elif line.find('3-GRAM') > 0:#(TAG1 TAG2 TAG3) counts of each tag trigram
                number, info, tagone, tagtwo, tagthree = line.split(' ')
                self.trigrams[(tagone.strip(), tagtwo.strip(), tagthree.strip())] = float(number)
        for x in self.trigrams.keys(): #(TAG1 TAG2 TAG3 | TAG1 TAG2)
            a, b, c = x
            self.calculated_trigram[x] = self.trigrams[x]/self.bigrams[(a,b)] #The conditional probability of a trigram given a bigram       

    def unigram_tagger(self, test_text):
        
        text = test_text.readlines()
        rare = ''
        tag_total = self.unigrams['I-GENE'] + self.unigrams['O'] #All tags
        rgene = self.emissions[('_RARE_', 'I-GENE')]/self.unigrams['I-GENE'] # The conditional probability of a rare word being a gene
        ro = self.emissions[('_RARE_', 'O')]/self.unigrams['O'] # The conditional probability of a rare not being a gene
        if rgene > ro: #All rare words will be considered genes
            rare = 'I-GENE'
        elif ro > rgene: #All rare words will not be considered genes
            rare = 'O'
        for line in text:
            gene = 0.0
            ogene = 0.0
            word = line.strip()
            if len(word) > 0:
                if self.emissions.has_key((word, 'I-GENE')) and self.emissions.has_key((word, 'O')) == True: #Safety
                    if self.emissions[(word, 'I-GENE')] == self.emissions[(word, 'O')] == 0: self.results.append(word +' '+ rare)
                if self.emissions.has_key((word, 'I-GENE')): #
                    gene = self.emissions[(word, 'I-GENE')]/self.unigrams['I-GENE']
                if self.emissions.has_key((word, 'O')):
                    ogene = self.emissions[(word, 'O')]/self.unigrams['O']
                elif self.emissions.has_key((word, 'I-GENE')) == False and self.emissions.has_key((word, 'O')) == False: #Rare result for words that were not seen in training
                    self.results.append(word +' '+ rare)
                if gene > 0 or ogene > 0:#Chooses tag
                    if gene > ogene: self.results.append(word + ' I-GENE')
                    elif ogene > gene: self.results.append(word + ' O')
            elif len(word) == 0: #For blank lines
                self.results.append(word)

    def viterbi(self, lines):
        sentences = []
        sentence = []
        
        for line in lines:
            word = line.strip()
            if len(word) > 0: sentence.append(word)
            elif len(word) == 0:
                sentences.append(sentence)
                sentence = []
        for sentence in sentences:
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
                        score, tag = max([(pi[(k-1, u, v)] * self.calculated_trigram[(u,v,w)] * self.emission_calculator((x,w)), u) for u in s[k-2]]) #Gets the most likely tag and its score based on all prior scores of bigram tags and the probability of the individual tag based on the word
                        pi[(k,v,w)] = score
                        back_pointer[(k,v,w)] = tag
            
                                   
            score, vtag, wtag = max([(pi[(len(sentence)-1, v, w)] * self.calculated_trigram[(v,w,"STOP")], v, w) for v in ['I-GENE', 'O'] for w in ['I-GENE', 'O']]) #Final prob
            pi[(len(sentence),wtag,'STOP')] = score 
            back_pointer[(len(sentence),w,'STOP')] = wtag #Back pointer's final tag
            y[len(sentence)-2] = vtag #Penultimate tag
            y[len(sentence)-1] = wtag #Final tag
            


            for k in xrange(len(sentence)-3, -1, -1): #Iterate backwards through the backpointer
                y[k] = back_pointer[(k+2,y[k+1],y[k+2])] #Finds the tag based on the two which follow it in the back pointer
            for x in xrange(0, len(sentence)): #Print out word tag pairs starting at the beginning of the sentence
                self.results.append(sentence[x] + ' ' +y[x])
#		print sentence[x] + ' ' + y[x]
            self.results.append(' ')
            
                
                    


    def emission_calculator(self, word_tuple):
        word, tag = word_tuple
        score = 0.0 #Defaults to send a probability of 0 for all words and will be changed
        if self.emissions.has_key((word, tag)):
            score = self.emissions[(word, tag)]/self.unigrams[tag]
        elif self.emissions.has_key((word, 'I-GENE')) == False and self.emissions.has_key((word, 'O')) == False: #Words not found in training data are calculated as a rare word
            nword = self.rare_replacer(word)#Replaces rare word with a class of rare words
            score = self.emissions[(nword, tag)]/self.unigrams[tag]  #Calculates prob based on type of rare word
        return score
    
    def rare_replacer(self, word): #Replace rare words with classes of words
        if len(word) > 2 and word[-1].isupper(): #All words ending in capitals
            if word[-2].isupper() == False: word = '_LCAPITAL_' #Words which end in a capital letter
            elif word.isupper(): word = '_ACAPITAL_' #Words that are completely capital
            elif re.findall('[0-9]', word): word = '_NUMERIC_' #Words that have numbers in them
            else: word = '_RARE_' #Generic rare
        elif re.findall('[0-9]', word): word = '_NUMERIC_'#Words that have numbers in them
        else: word = '_RARE_' #Generic rare
        return word

    def write_results(self, output):
            for line in self.results:            
                output.write("%s\n" % (line))



if __name__ == "__main__":


    try:
        training_lines = file(sys.argv[1],"r")
        test_text = file(sys.argv[2], 'r')
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    # Initialize a trigram counter
    HMM = HMM_Tagger(training_lines)
    # Collect counts
    #output = HMM.unigram_tagger(test_text)
    output = HMM.viterbi(test_text)
    # Write the counts
    HMM.write_results(sys.stdout)
