


def simpleqsort(Xs):
    if len(Xs) <= 1:
        return Xs
    i,Xs = pivotsort(Xs)
    return simpleqsort(Xs[:i]) + [Xs[i]] + simpleqsort(Xs[i+1:])#must recurse on smaller arrays




def pivotsort(Xs):
    pivot = Xs[0]
    i = 1
    for j in xrange(1, len(Xs)):
        if Xs[j] < pivot:
           Xs[j], Xs[i] = Xs[i], Xs[j]
           i+=1
    Xs[0],Xs[i-1]=Xs[i-1],Xs[0]#if i =1, no change
    return (i-1,Xs)
    






if __name__=="__main__":
   Xs = [1,3,2,5,4,6,0]
   print simpleqsort(Xs)
