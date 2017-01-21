import numpy as np 
# ADDME 
# Description: Module which contains all relevent ILP
#              functions. 
#                     (1) ILP()  
###########################################################


###########################################################
# Description:
#       Function to create the objective function.
#       Due to the size of the obj function, it will
#       be constructed in parts, each part representing
#       the sum terms or constraints formulas.
# Inputs:
#        R   :: The request matrix
#        D   :: The total number of destinations
#        K   :: The total number of nodes
#        M   :: The total number of nodes
#        L   :: Set of vNF
#        F   :: Set containing the functions
#        Sr  :: Set of starting nodes of each chain 
#        u   :: vecotr of vNF typ i requirements 
# Return:
#    obj   :: The composition of each summation term
#               in the objective function.
#      A   :: The Linear inequality constraint matrix,
#             specified as a matrix of doubles.
#      b   :: The Linear inequality constraint vector,
#             specified as a vector of doubles.
#    Aeq   :: The Linear equality constraint matrix,
#             specified as a matrix of doubles.
#    beq   :: The Linear equality constraint vector,
#             specified as a vector of doubles.
#     lb   :: The Lower bounds, specified as an array
#             of doubles.
#     ub   :: The Upper bounds, specified as an array
#             of doubles.
#  intcon  :: The Vector of integer constraints, specified
#             as a vector of positive integers.
###########################################################
def makeOBJ(K,L,R,P,V,C,Dk,Sr,rho):
    debug = 0  

    #Get the size of the request
    row,col = R.shape
    S = len(Sr)
    M = K
    D = len(Dk)
    lengthOfrequest = col
    #Ln= L              # The final value of L

    # Objective Function :: obj
    # Allocate vector size
    f1=np.zeros((row,K,L))
    f2=np.zeros((row,S,D,K,L))
    f3=np.zeros((row,S,D,K,M,L,L,col-1))
    F3=np.zeros((row,S,D,K,M,L,L))
    f4=np.zeros((row,S,D,K,L))

    # The first term
    for rr in range(0, row-1):
        for kk in range(0,K-1):
            for ii in range(0,L-1):
                f1[rr,kk,ii] = C[kk,ii]
    #END FOR(1) 

    print f1 

    # Second term
    for rr in range(0,row-1): 
        for ss in range(0,S):
            for dd in range(0,D): 
                for kk in range(0,K-1):
                    for ii in range(0,L-1): 
                        f2[rr,ss,dd,kk,ii]=rho[dd]*P[ss,kk]*V[rr,ii,0]
    # END FOR (2) 
    
    print len(f2.flatten())
    

    # Third term
    #for rr in range(0,row-1):
    #    for ss in range(0,S-1):
    #        for dd in range(0,D-1):
    #            for kk in range(0,K-1):
    #                for mm in range(0,M-1):
    #                    for ii in range(0,L-1):
    #                        for jj in range(0,L-1):
    #                            #for ll in range(0,L-2):
    #                            for ll in range(0, col - 2):
    #                                f3[rr,ss,dd,kk,mm,ii,jj,ll]=rho[dd]*P[kk,mm]*V[rr,ii,ll]*V[rr,ii,ll+1]

    for rr in range(0, row - 1):
        for ss in range(0, S - 1):
            for dd in range(0, D - 1):
                for kk in range(0, K - 1):
                    for mm in range(0, M - 1):
                        for ii in range(0, L - 1):
                            for jj in range(0, L - 1):
                                for ll in range(0, col - 2):
                                    f3[rr,ss,dd,kk,mm,ii,jj,ll] = rho[dd] * P[kk,mm] * V[rr,ii,ll] * V[rr,ii,ll + 1]
                                    F3[rr,ss,dd,kk,mm,ii,jj] = F3[rr,ss,dd,kk,mm,ii,jj] + f3[rr, ss,dd,kk, mm, ii,jj,ll]
    # END FOR (3) 

    # Fourth term
    for rr in range(0,row-1): 
        for ss in range(0,S-1): 
            for dd in range(0,D-1): 
                for kk in range(0,K-1):
                    for ii in range(0,L-1):
                        #f4[rr,ss,dd,kk,ii]=rho[dd]*P[ss,kk]*V[rr,ii,col-1]
                        f4[rr, ss, dd, kk, ii] = rho[dd] * P[kk, dd] * V[rr, ii, col - 1]
                        print
    # END FOR (4) 

    F1=f1
    F2=f2+f4
    F3=F3
    # Flatten all the all of the vectors and put into a single vector                         
    #obj = np.hstack((f1.flatten(),f2.flatten(),f3.flatten(),f4.flatten()))
    obj = np.hstack((F1.flatten(), F2.flatten(), F3.flatten()))

    if(debug): 
        print "In makeObjective:"
        print "Length: ", len(obj)

    
    return obj , f1.flatten(),f2.flatten(), f3.flatten(), f4.flatten(),

def makeOBC(K,L,R,P,V,C,Dk,Sr,u,U,rho):
    # Get the size of the request
    row, col = R.shape
    S = len(Sr)
    M = K
    D = len(Dk)
    LOR = col # Length of requests


    # Linear inequality constraint matrix :: A
    # Allocate matrix size
    A = np.zeros(((2 * K + row * S * D * col + row * S * D * K * L + 3 * row * S * D * K * K * L * L),
                  (row * K * L + row * S * D * K * L + row * S * D * K * M * L * L)))

    # 6(a)
    for kk in range(0, K - 1):
        for rr in range(0, R - 1):
            for ii in range(0, L - 1):
                A[kk, (rr - 1) * K * L + (kk - 1) * L + ii] = u[0, kk]
                A[K+kk, (rr - 1) * K * L + (kk - 1) * L + ii] = u[1, kk]
    #END FOR 6(a)

    # 6(b)
    for rr in range(0, row-1):
        for ss in range(0, S-1):
            for dd in range(0, D-1):
                for ll in range(0, LOR-1):
                    for kk in range(0, K-1):
                        for ii in range(0, L-1):
                            A[(2*K+(rr-1)*S*D*LOR+(ss-1)*D*LOR+(dd-1)*LOR+ll),(row*K*L+(rr-1)*S*D*K*L+(ss-1)*D*K*L+(dd-1)*K*L+(kk-1)*L+ii)] = (-1)*V[rr-1,ll-1,ii-1]
    #END FOR 6(b)

    # 6(c)
    for rr in range(0, row-1):
        for ss in range(0, S-1):
            for dd in range (0, D-1):
                for kk in range(0, K-1):
                    for ii in range(0, L-1):
                        A[(2*K+row*S*D*LOR+(rr-1)*S*D*K*L+(ss-1)*D*K*L+(dd-1)*K*L+(kk-1)*L+ii),((rr-1)*K*L+(kk-1)*L+ii)] = 1
                        A[(2*K+row*S*D*LOR+(rr-1)*S*D*K*L+(ss-1)*D*K*L+(dd-1)*K*L+(kk-1)*L+ii),(row*K*L+(rr-1)*S*D*K*L+(ss-1)*D*K*L+(dd-1)*K*L+(kk-1)*L+ii)] = (-1)
    #END FOR 6(c)

    # 6(d)
    for rr in range(0, row-1):
        for ss in range(0, S-1):
            for dd in range(0, D-1):
                for mm in range(0, K-1):
                    for kk in range(0, K-1):
                        for jj in range(0, L-1):
                            for ii in range(0, L-1):
                                A[(2*K+row*S*D*LOR+row*S*D*K*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii),(row*K*L+row*S*D*K*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii)] = 1
                                A[(2*K+row*S*D*LOR+row*S*D*K*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii),(row*K*L+(rr-1)*S*D*K*L+(ss-1)*D*K*L+(dd-1)*K*L+(kk-1)*L+ii)] = (-1)
    #END FOR 6(d)

    # 6(e)
    for rr in range(0, row-1):
        for ss in range(0, S-1):
            for dd in range(0, D-1):
                for mm in range(0, K-1):
                    for kk in range(0, K-1):
                        for jj in range(0, L-1):
                            for ii in range(0, L-1):
                                A[(2*K+row*S*D*LOR+row*S*D*K*L+row*S*D*K*K*L*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii),(row*K*L+row*S*D*K*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii)] = 1
                                A[(2*K+row*S*D*LOR+row*S*D*K*L+row*S*D*K*K*L*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii),(row*K*L+(rr-1)*S*D*K*L+(ss-1)*D*K*L+(dd-1)*K*L+(mm-1)*L+jj)] = (-1)
    #END FOR 6(e)

    # 6(f)
    for rr in range(0, row-1):
        for ss in range(0, S-1):
            for dd in range(0, D-1):
                for mm in range(0, K-1):
                    for kk in range(0, K-1):
                        for jj in range(0, L-1):
                            for ii in range(0, L-1):
                                A[(2*K+row*S*D*LOR+row*S*D*K*L+2*row*S*D*K*K*L*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii),(row*K*L+row*S*D*K*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii)] =(-1)
                                A[(2*K+row*S*D*LOR+row*S*D*K*L+2*row*S*D*K*K*L*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii),(row*K*L+(rr-1)*S*D*K*L+(ss-1)*D*K*L+(dd-1)*K*L+(kk-1)*L+ii)] = 1
                                A[(2*K+row*S*D*LOR+row*S*D*K*L+2*row*S*D*K*K*L*L+(rr-1)*S*D*K*K*L*L+(ss-1)*D*K*K*L*L+(dd-1)*K*K*L*L+(mm-1)*K*L*L+(kk-1)*L*L+(jj-1)*L+ii),(row*K*L+(rr-1)*S*D*K*L+(ss-1)*D*K*L+(dd-1)*K*L+(mm-1)*L+jj)] = 1
    #END FOR 6(f)

    # Linear inequality constraint vector :: b
    # Allocate matrix size
    b = np.zeros((2*K+row*S*D*LOR+row*S*D*K*L+3*row*S*D*K*K*L*L),1)

    # 6(a)
    b[0:K-1, 0] = U[0, 0:K-1]
    b[K:2*K-1, 0] = U[1, 0:K-1]

    # 6(b)
    b[2*K:2*K+row*S*D*LOR-1, 0] = (-1)

    # 6(c)
    b[2*K+row*S*D*LOR:2*K+row*S*D*LOR+row*S*D*K*L-1, 0] = 0

    # 6(d)
    b[2*K+row*S*D*LOR+row*S*D*K*L:2*K+row*S*D*LOR+row*S*D*K*L+row*S*D*K*K*L*L-1, 0] = 0

    # 6(e)
    b[2*K+row*S*D*LOR+row*S*D*K*L+row*S*D*K*K*L*L:2*K+row*S*D*LOR+row*S*D*K*L+2*row*S*D*K*K*L*L-1, 0] = 0

    # 6(f)
    b[2*K+row*S*D*LOR+row*S*D*K*L+2*row*S*D*K*K*L*L:2*K+row*S*D*LOR+row*S*D*K*L+3*row*S*D*K*K*L*L-1, 0] = 1

    # Vector of integer constraints :: intcon
    # Allocate matrix size
    intcon = np.zeros(1, (row*K*L+row*S*D*K*L+row*S*D*K*K*L*L))

    for nn in range(0,row*K*L+row*S*D*K*L+row*S*D*K*K*L*L-1):
        intcon[0,nn] = nn

    # Lower bounds :: lb
    lb = np.zeros((row*K*L+row*S*D*K*L+row*S*D*K*K*L*L), 1)

    # Upper bounds :: ub
    ub = np.ones((row*K*L+row*S*D*K*L+row*S*D*K*K*L*L), 1)

    # Linear equality constraint matrix :: Aeq
    Aeq = []

    # Linear equality constraint vector :: beq
    beq = []

    return A, b, intcon, lb, ub, Aeq, beq