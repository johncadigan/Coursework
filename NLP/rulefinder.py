from nltk.corpus import treebank
import re

symbols = "\.\,\'\"\*\$\-\?\%\&"
rule = "[A-Z0-9{0}]".format(symbols) + "{1,10}"
word = "[\w*{0}]".format(symbols) + "{1,20}"

def balanced_parens(sent):
    rgt = sent.count("(")
    lft = sent.count(")")
    if lft==rgt and lft > 0:
        return True
    else:
        return False

def find_nonunary(sent):
    parent = re.findall("(\({0})".format(rule), sent)[0][1:]
    fblank = sent.find(parent)+len(parent)#find first blank
    rules = []
    children = []
    start_rule = int(fblank)
    end_rule = int(fblank)
    while end_rule < len(sent):
        end_rule+=1
        section = sent[start_rule:end_rule]
        if balanced_parens(sent[start_rule:end_rule]):
            next_children = re.findall("(\({0})".format(rule), section)
            if len(next_children) > 0:
                child = next_children[0][1:]
                children.append(child)
                if len(next_children) > 1:
                    rules+=(find_nonunary(section))
                start_rule=int(end_rule)
    rules.append("{0} -> {1}".format(parent, " ".join(children)))
    return rules
    

def find_unary(sent):
    rules = []
    results = re.findall("(\({0}\ {1}\))".format(rule,word), sent)
    for res in results:
        x = res.split(" ")
        if len(x) == 2:
            p,c = x
            rules.append("{0} -> '{1}'".format(p[1:], c[:-1]))
    return rules

def check(productions, rules):
    i = 0
    for x in productions:
        if str(x) in rules: i += 1
        else: print x
    return (i,len(productions))

if __name__=="__main__":
   total, recall = 0,0
   for s in treebank.parsed_sents():
        sent = "".join(str(s).split("\n"))
        unaries = find_unary(sent)
        nonunaries = find_nonunary(sent)
        rules = unaries + nonunaries
        r, t = check(s.productions(), rules)
        recall+=r
        total+=t
   print "{0} out of {1}: {2}".format(recall,total, float(recall)/total)
   


