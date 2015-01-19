import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys
import unittest


class Peak(object):


    def __init__(self, f):
        v = f.readlines()
        self.v = [float(l) for l in v]
        self.fig = plt.figure()
        ax1 = self.fig.add_subplot(1,1,1)
        ax1.plot(range(0, len(self.v)), self.v, color='b', label = 'original')
   
    def plot(self):
        plt.show()

class NoisyPeak(Peak):

     def __init__(self, f):
         super(NoisyPeak, self).__init__(f)
         self.preprocess()
    
     def remove_linear(self):#Removes increase through linear regression
         slope, y0 = np.polyfit(range(1, len(self.v)+1), self.v,1)
         self.y = [p-slope*i-y0 for i,p in enumerate(self.v)]
         ax2 = self.fig.add_subplot(1,1,1)
         ax2.plot(range(0, len(self.v)), self.y, 'r--') 
         print "New mean {0}".format(np.mean(self.y))
     
     def standard_devs(self):#Calculates each point's standard deviation up to that point
         sd = [0.0]         
         sd += [self.y[x]/np.std(self.y[0:x]) for x in range(1, len(self.y))]
         ax3 = self.fig.add_subplot(1,1,1)
         ax3.plot(range(0, len(self.v)), sd, color='g', label='noise')
         self.sd = sd


     def preprocess(self):#Cleans data
         self.remove_linear()
         self.standard_devs()

     def solve_for(self, n, dsd=.25):#Solves for n peaks
         sd = 1.0
         res = [i for i,y in enumerate(self.y) if self.y[i-1] < self.y[i] > self.y[i+1] and self.sd[i] > sd]
         while(len(res) > n):
             sd+=dsd
             res = [i for i in res if self.y[i] > sd]
         return res



if __name__ == "__main__":
     f = file(sys.argv[1], "r")
     n = int(sys.argv[2])
     p = NoisyPeak(f)
     print p.solve_for(n)
     p.plot()

