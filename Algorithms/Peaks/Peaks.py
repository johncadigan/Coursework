import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys
import unittest

SD_THRESHOLD = 3.0
FILE = "PeakFindingData.csv" 

class Peak(object):


    def __init__(self, l):
        self.v = l
        self.fig = plt.figure()
        ax1 = self.fig.add_subplot(1,1,1)
        ax1.plot(range(0, len(self.v)), self.v, color='b', label = 'original')
    
    @classmethod
    def from_file(cls, f):
        l = [float(l) for l in f.readlines()]
        return cls(l)

    def plot(self):
        plt.show()

class NoisyPeak(Peak):

     def __init__(self, l, verbose =False):
         self.verbose = verbose
         super(NoisyPeak, self).__init__(l)
         self.preprocess()     

 
     def remove_linear(self):#Removes increase through linear regression
         slope, y0 = np.polyfit(range(1, len(self.v)+1), self.v,1)
         self.y = [p-slope*i-y0 for i,p in enumerate(self.v)]
         if self.verbose:
             ax2 = self.fig.add_subplot(1,1,1)
             ax2.plot(range(0, len(self.v)), self.y, 'r--') 
     
     def standard_devs(self):#Calculates each point's standard deviation up to that point          
         sd = [self.y[x]/np.std(self.y[0:x]) if np.std(self.y[0:x]) > 0.0 else 0.0 for x in range(0, len(self.y))]
         self.sd = sd
         if self.verbose:
             ax3 = self.fig.add_subplot(1,1,1)
             ax3.plot(range(0, len(self.v)), sd, color='g', label='noise')
         
     def preprocess(self):#Cleans data
         self.y = self.v
         self.remove_linear()
         self.standard_devs()

     def filter(self, xs, sd):
         res = [i for i in xs if self.y[i-1] < self.y[i] > self.y[i+1] and self.sd[i] > sd]
         return res

     def solve_for(self, n, dsd=.25):#Solves for n peaks
         sd = 1.0
         res = self.filter(range(0, len(self.y)), sd)
         while(len(res) > n):
             sd+=dsd
             res = [i for i in res if self.y[i] > sd]
         return res

     def solve(self):
         res = self.filter(range(0, len(self.y)), SD_THRESHOLD)
         for x in res:
             print x, self.sd[x]
         return res

class WNoisyPeak(NoisyPeak):

     def __init__(self, w, l):
         self.w = w
         super(WNoisyPeak, self).__init__(l)

     def standard_devs(self):
         w = self.w
         sd = [self.y[x]/np.std(self.y[0:w*2]) for x in range(0,w)] # initial
         sd += [self.y[x]/np.std(self.y[x-w:x+w]) if np.std(self.y[0:x]) > 0.0 else 0.0 for x in range(w, len(self.y)-w*2)]
         sd += [self.y[x]/np.std(self.y[len(self.y)-w*2:len(self.y)]) for x in range(len(self.y)-2*w, len(self.y))]
         self.sd = sd
         if self.verbose:
             ax3 = self.fig.add_subplot(1,1,1)
             ax3.plot(range(0, len(self.v)), sd, color='g', label='noise')
 



class TestTests(unittest.TestCase):  
     
     def setUp(self):
       lines = open(FILE).readlines()
       self.values = [float(l) for l in lines]
     
     def test_one(self):
        t = NoisyPeak(self.values)
        self.assertTrue(t.solve()==[17, 140, 304, 484])
    
     def test_two(self):
        t = WNoisyPeak(36, self.values)
        t.solve()
        self.assertTrue(t.solve()==[17,140,304,484])

"""
if __name__ == "__main__":
     f = file(sys.argv[1], "r")
     p = NoisyPeak.from_file(f)
     if len(sys.argv) == 3:
         print p.solve_for(int(sys.argv[2]))
     else:
         print p.solve()
     p.plot()

"""
if __name__ == "__main__":
    unittest.main()

