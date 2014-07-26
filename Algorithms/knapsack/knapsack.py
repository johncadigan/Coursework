import sys
from collections import defaultdict
import unittest
import itertools
import random

class Knapsack(object):


     def __init__(self, lines):
         self.verbose = False
         capacity, no_items = lines[0].split(" ")
         self.capacity = int(capacity)
         self.weights = {}
         self.values = {}
         self.A = defaultdict(dict)
         self.A = {i: {} for i in xrange(0, int(no_items)+1)}
         items = [] 
         for line in lines[1:]:
             value, weight = line.split(" ")
             items.append((int(value), int(weight)))
         items = sorted(items, key=lambda a: float(a[0])/float(a[1]), reverse=True)
         for i, item in enumerate(items):
             value, weight = item
             self.weights[i+1] = weight
             self.values[i+1] = value
         self.A[1][0] = 0
         self.A[0][0] = 0 
     
     def main(self):
         for i in xrange(1,len(self.values)+1):
             if self.verbose: print "Item {0} w{1} v{2}".format(i, self.weights[i], self.values[i]) 
             cur_weights = sorted(self.A[i].keys())
             for n, x in enumerate(cur_weights):
                 #Updating old values
                 if x-self.weights[i] >= 0:
                      if self.A[i-1].has_key(x-self.weights[i]):
                          lower_w_v = self.A[i-1][x-self.weights[i]]
                      else:
                          l = filter(lambda a: a < x-self.weights[i], self.A[i-1].keys())
                          l.sort()
                          lower_w_v = self.A[i-1][l[-1]]
                      self.A[i][x] = max(self.A[i-1][x], lower_w_v+self.values[i])
                 else:
                      self.A[i][x] = self.A[i-1][x]
                 #Adding new values based on current item
                 new_weight = x+self.weights[i]
                 last_weight = sorted(filter(lambda a: a < new_weight, cur_weights))[-1]
                 new_value = self.values[i]+self.A[i][last_weight]
                 if self.A[i].has_key(new_weight)== False and new_weight <= self.capacity and self.A[i][last_weight] < new_value:
                      if self.verbose: print "Adding new weight ", x+self.weights[i]
                      self.A[i][x+self.weights[i]] = self.A[i][x] + self.values[i]                 
             if i+1 <= len(self.values): self.A[i+1] = self.A[i]
             if i > 2: del self.A[i-2]
             if self.verbose: print "i :", i, self.A
         return max(self.A[len(self.values)].values())

                     




class TestTests(unittest.TestCase):
    
    def setUp(self):
        pass   
    
    def test_one(self):
        lines = "6 4\n3 4\n2 3\n4 2\n4 3".split("\n")
        k = Knapsack(lines)
#        k.verbose = True
        self.assertTrue(k.main()==8)

    def test_two(self):
        lines = "6 3\n3 2\n3 3\n1 1".split("\n")
        k = Knapsack(lines)
        k.verbose = True
        self.assertTrue(k.main()==7)

    def test_three(self):
        lines = "100 10\n10 70\n10 60\n10 50\n10 40\n10 30\n10 20\n10 10\n10 5\n10 2\n10 1".split("\n")
        k1 = Knapsack(lines)
        random_lines = lines[1:]
        random.shuffle(random_lines)
        k2 = Knapsack([lines[0]]+random_lines)
        self.assertTrue(k1.main()==k2.main())
        k3 = Knapsack(lines)
        self.assertTrue(k3.main()==60)

    def four(self):
        lines = '106925262 106\n45276 45276\n90552 90552\n181104 181104\n362208 362208\n724416 724416\n1448832 1448832\n2897664 2897664\n5795328 5795328\n11590656 11590656\n23181312 23181312\n46362624 46362624\n92725248 92725248\n70778 70778\n141556 141556\n283112 283112\n566224 566224\n1132448 1132448\n2264896 2264896\n4529792 4529792\n9059584 9059584\n18119168 18119168\n36238336 36238336\n72476672 72476672\n86911 86911\n173822 173822\n347644 347644\n695288 695288\n1390576 1390576\n2781152 2781152\n5562304 5562304\n11124608 11124608\n22249216 22249216\n44498432 44498432\n88996864 88996864\n92634 92634\n185268 185268\n370536 370536\n741072 741072\n1482144 1482144\n2964288 2964288\n5928576 5928576\n11857152 11857152\n23714304 23714304\n47428608 47428608\n94857216 94857216\n97839 97839\n195678 195678\n391356 391356\n782712 782712\n1565424 1565424\n3130848 3130848\n6261696 6261696\n12523392 12523392\n25046784 25046784\n50093568 50093568\n100187136 100187136\n125941 125941\n251882 251882\n503764 503764\n1007528 1007528\n2015056 2015056\n4030112 4030112\n8060224 8060224\n16120448 16120448\n32240896 32240896\n64481792 64481792\n134269 134269\n268538 268538\n537076 537076\n1074152 1074152\n2148304 2148304\n4296608 4296608\n8593216 8593216\n17186432 17186432\n34372864 34372864\n68745728 68745728\n141033 141033\n282066 282066\n564132 564132\n1128264 1128264\n2256528 2256528\n4513056 4513056\n9026112 9026112\n18052224 18052224\n36104448 36104448\n72208896 72208896\n147279 147279\n294558 294558\n589116 589116\n1178232 1178232\n2356464 2356464\n4712928 4712928\n9425856 9425856\n18851712 18851712\n37703424 37703424\n75406848 75406848\n153525 153525\n307050 307050\n614100 614100\n1228200 1228200\n2456400 2456400\n4912800 4912800\n9825600 9825600\n19651200 19651200\n39302400 39302400\n78604800 78604800'.split("\n")
        k = Knapsack(lines)
        #k.verbose = True
        self.assertTrue(k.main()==106925262)

if __name__=='__main__':
    try:
        k_list = file(sys.argv[1],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    K = Knapsack(k_list.readlines()[0:501])
    print K.main()
"""
if __name__ == '__main__':
   unittest.main()
"""
