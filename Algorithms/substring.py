

def findss(s1, s2):
    A = [[0]*(len(s1)+1) for x in range(len(s2)+1)]
    B = {} #backpointer
    mx = 0
    matches = 0
    for j in range(0, len(s2)):#row first
        for k in range(0, len(s1)):
            m = s2[j]
            n = s1[k]
            if m == n:
                matches +=1
                if j==0 or k == 0:
                     A[j+1][k+1] = 1
                else:
                     A[j+1][k+1] = A[j][k] +1
                if A[j+1][k+1] > mx:
                    mx = A[j+1][k+1]
                    B[mx] = (j+1, k+1)
    i,j = B[mx]
    return s1[i-mx:i]


if __name__ == "__main__":
    Xs = [("iron", "irony"), ("irony", "iron"), ("baba", "abab"), ("abab", "baba")]
    for x in Xs:
        print findss(x[0], x[1])
