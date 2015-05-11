from nltk.corpus import treebank
import re

def reduce_to_rules(tree_string):
    tree_string = "".join(tree_string.split("\n"))
    all_rules = "".join(re.findall("(\([A-Z]{1,4}|\(\.|\(\,|\(|\))", tree_string))
    assert(all_rules.count("(") == all_rules.count(")")) 
    return all_rules

def reduce_to_urules(tree_string):
    tree_string = "".join(tree_string.split("\n"))
    all_unary = re.findall("(\([A-Z]{1,4} \w*\.?\))", tree_string)
    rules = []
    for x in all_unary:
        p, c = x.split(" ")
        p = p[1:]
        c = c[:len(c)-1]
        rules.append("{0} -> '{1}'".format(p, c))
    return rules


def balanced_paren(p_string):
    rgt = p_string.count("(")
    lft = p_string.count(")")
    return lft > 0 and rgt == lft

def extract_rule(rule_string):
    if rule_string.find("(",1) >= 0:
        second_paren = rule_string.index("(",1)
        rules = True
    else:
        second_paren = rule_string.index(")")
        rules = False
    parent = rule_string[1:second_paren]
    return (parent, second_paren, rule_string, rules)

def non_unary_rules(rule_string):
    parent, nextr, rs, rules =  extract_rule(rule_string)
    rule_exp = []
    children = []
    i = nextr
    while i < len(rule_string):
         i+=1
         if balanced_paren(rule_string[nextr:i]) and len(rule_string[nextr:i]) >1:
            child, n, rs, rules = extract_rule(rule_string[nextr:i])
            if rules: rule_exp += non_unary_rules(rs)
            nextr = i
            children.append(child)
    rule_exp += ["{0} -> {1}".format(parent, " ".join(children))]
    return rule_exp
            
            
def check(productions, rules):
    i = 0
    for x in productions:
        simple = re.sub("(\-[A-Z]{1,4})", "", str(x))
        if simple in rules: i += 1
        else: print simple
    print "{0}/{1}".format(i, len(productions))
        


if __name__=="__main__":
   sent = str(treebank.parsed_sents()[1])
   r = reduce_to_urules(sent)
   rules = reduce_to_rules(sent)
   r+= non_unary_rules(rules)
   
   check(treebank.parsed_sents()[1].productions(), r)
