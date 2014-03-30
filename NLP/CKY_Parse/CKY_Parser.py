import sys
from collections import defaultdict
from math import log
import re
import json

class CKY_Parser():
    
    def __init__(self, training_text):
        self.results = []
        self.binary_rules = {}
        self.birule_prob = {}
        self.unrule_prob = {}
        self.unary_rules = {}
        
        self.nonterminals = {}
        self.words = {}
        self.get_children = {}
        
        lines = training_text.readlines()
        for line in lines:
            if line.count('NONTERMINAL'): #Stores the overall occurences of rules
                number, info, symbol = line.split(' ')
                number = int(number)
                symbol = symbol.strip()
                self.nonterminals[symbol] = number
            elif line.count('UNARYRULE'): #Stores the rules which tag a word
                number, info, tag, word = line.split(' ')
                number = int(number)
                word = word.strip()
                self.words[word] = True
                self.unary_rules[(word, tag)] = number
            elif line.count('BINARYRULE'): #Stores the rules which combine two tags under a parent
                number, info, parent, tag1, tag2 = line.split(' ')
                number = int(number)
                tag2 = tag2.strip()
                self.binary_rules[(parent, tag1, tag2)] = number
                self.get_children.setdefault(parent, [])
                self.get_children[parent].append((tag1, tag2)) #add pair of tags to all possible children for the parent
                
        for key in self.binary_rules.keys():#Calculate and store probability for binary rules
            parent, tag1, tag2 = key
            self.birule_prob[key] = float(self.binary_rules[key])/float(self.nonterminals[parent])
        
        for key in self.unary_rules.keys(): #Calculate and store probability for unary rules
            word, tag = key
            self.unrule_prob[key] = float(self.unary_rules[key])/float(self.nonterminals[tag])
    
    
    def branch_build(self, backpointer, i, j, parent, sentence): #Recursively builds the tree branch
            if i == j: 
                return [parent, sentence[i].strip()]
            else:
                s, tag1, tag2 = backpointer[(i,j,parent)]
                return [parent, self.branch_build(backpointer, i, s, tag1, sentence), self.branch_build(backpointer, s+1, j, tag2, sentence)] #Adds branches below each child
        
            
    def tree_build(self, backpointer, sentence): #Builds the tree
        i = 0
        j = len(sentence) - 1
        tree = self.branch_build(backpointer, i, j, 'SBARQ', sentence) 
        return tree

    
    def parse(self, input):
        sentences = []
        sentence = []
        
        lines = input.readlines()
        for line in lines:
            sentence = line.split(' ')
            sentences.append(sentence)
        
        for sentence in sentences:
            n = len(sentence)
            pi = {}#Stores probability up to this point; name from pseudo code
            backpointer = {}
            #intialization with all possible tags for a given word
            for i in xrange(0, len(sentence)):
                for tag in self.nonterminals.keys():
                    pi[i,i,tag] = 0.0 #Set to 0 for all tags
                    word = sentence[i].strip()
                    if self.unary_rules.has_key((word, tag)): 
                        pi[i, i, tag] = self.unrule_prob[(word, tag)] #Set probability if it is found in unary rules
                    elif self.words.has_key(word) == False and self.unrule_prob.has_key(("_RARE_",tag)): 
                        pi[i, i, tag] = self.unrule_prob[("_RARE_", tag)] #Set tag probability to possible rare token and tag pairs
            
            #fprint = False
            #if sentences.index(sentence)== 0: fprint = True #First sentence print is set to true/ From historical debugging
            
            printed_out = []
            for l in xrange(1, n):
                for i in xrange(0, n-l):
                    j = i+l
                    for parent in self.nonterminals.keys(): #Iterate through all tags
                        if self.get_children.has_key(parent): #Choose only those which have children, ie. binary rules.
                            score, max_s, max_parent, max_tag1, max_tag2 = max([(self.birule_prob[(parent, tag1, tag2)] * pi[(i,s,tag1)] * pi[(s+1,j,tag2)], s, parent, tag1, tag2) for s in xrange(i, j) for tag1, tag2 in self.get_children[parent]]) #Find the most probable tags for parent and children as well as where they split 
                            pi[(i, j, max_parent)] = score
## Historical debugging
##                            if fprint and i < 5 and j < 5: 
##                                print i, j,
##                                print [(self.birule_prob[(parent, tag1, tag2)] * pi[(i,s,tag1)] * pi[(s+1,j,tag2)], self.birule_prob[(parent, tag1, tag2)], pi[(i,s,tag1)], pi[(s+1,j,tag2)], s, parent, tag1, tag2) for s in xrange(i, j) for tag1, tag2 in self.get_children[parent]] 
                            backpointer[(i, j, max_parent)] = (max_s, max_tag1, max_tag2)
                        elif self.get_children.has_key(parent) == False: #Set all unary rules to 0
                            pi[(i,j, parent)] = 0.0
            
## Historical debugging
##            if fprint == True: 
##                for key in backpointer.keys():
##                    score, s, i, j, parent, tag1, tag2 = backpointer[key]
##                    if score > 0: print i, j, parent, tag1, tag2, s, score
            
            j = n-1
            i = 0
            score, max_s, max_tag1, max_tag2 = max([(self.birule_prob[('SBARQ', tag1, tag2)] * pi[(i,s,tag1)] * pi[(s+1,j,tag2)], s, tag1, tag2) for s in xrange(0, n-1) for tag1, tag2 in self.get_children['SBARQ']]) #Calculates final overall probabilities
            backpointer[(i, j, 'SBARQ')] = (max_s, max_tag1, max_tag2) #Final backpointer state
            tree = self.tree_build(backpointer, sentence) #Builds tree
            self.results.append(json.dumps(tree)) #Appends to results


## Historical debugging            
##            if fprint == 3:
##                print 'Maximum', 'i', 0, 'j', n-1, 's', max_s, 'tag1', max_tag1, 'tag2', max_tag2            
##                for x in pi.keys():
##                            if pi[x] > 0 and printed_out.count((x,pi[x])) == 0: 
##                                print x, pi[x]
##                                printed_out.append((x,pi[x]))
##                                if backpointer.has_key(x): print 'backpointer', backpointer[x] 
            
    
    
    



    def write_results(self, output):
        
        for line in self.results:            
            output.write("%s\n" % (line))

if __name__ == "__main__":

    try:
        training_text = file(sys.argv[1],"r")
        test_text = file(sys.argv[2], 'r')
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    # Initialize with training data
    CKY = CKY_Parser(training_text)
    # Collect counts
    output = CKY.parse(test_text)
    # Write the counts
    CKY.write_results(sys.stdout)
