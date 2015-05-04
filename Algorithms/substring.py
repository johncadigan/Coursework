
def find_ss(s1, s2):
	A = [[0]*(len(s1)+1)]
        A += [[0]+len(s1)*[0]]*(len(s2)+1)# rows = ss columns = s
        ml = 0 #max length
        B = {} #backpointer
        for i in xrange(1, len(s1)+1):
            for j in xrange(1, len(s2)+1):
                l = s1[i-1]
                m = s2[j-1]
                if l == m: #a match
                    if i == 0 or j == 0:#first row or column
                        A[i][j] = 1
                    else: #consider previous
                        A[i][j] = A[i-1][j-1] + 1
                if A[i][j] > ml:#create backpointer
                    ml = A[i][j]
                    B[ml] = (i,j) 
        return B

if __name__=="__main__":
     s = "abab"
     ss = "baba"
     B =  find_ss(s, ss)
     mv = max(B.keys())
     i, j = B[mv]
     print ss[i-mv:i]
