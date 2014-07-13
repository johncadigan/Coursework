import sys

class JobScheduler(object):

    def __init__(self, job_list):
        self.job_list = job_list
    
    def sub_schedule(self):
        job_sub_list = map(lambda a: (a,a[0]-a[1]), job_list)
        
        #Sorting with two keys, the first is the difference and the second
        #is the weight
        ordered_job_sub = sorted(job_sub_list, key= lambda a: (a[1],a[0][0]), reverse=True)
        self.job_list = map(lambda a: a[0], ordered_job_sub)
        
    def ratio_schedule(self):
        self.job_list = sorted(job_list, key=lambda a: float(a[0])/a[1], reverse=True)


    def score(self):
         i = 0
         score = 0
         for x in self.job_list:
             weight, length = x
             i += length
             score+=i*weight
         return score
             
        

if __name__=='__main__':
    try:
        j_list = file(sys.argv[1],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    job_lines = j_list.readlines()
    #Turn the lines into tuples of job weight and length
    #job_lines = "50\t18\n10\t44\n94\t8\n30\t26\n98\t68\n78\t6\n2\t56\n54\t20\n30\t40\n56\t62\n60\t22\n92\t10\n98\t52\n4\t52\n80\t36\n12\t88\n32\t86\n8\t88".split('\n')
    job_list = [tuple([int(b) for b in a.split(' ')]) for a in job_lines]
    
    j = JobScheduler(job_list)
    j.sub_schedule()
    print "Cost via subtraction scheduling {0}".format(j.score())
    j.ratio_schedule()
    print "Cost via ratio scheduling {0}".format(j.score())
    #ratio schedule
    
