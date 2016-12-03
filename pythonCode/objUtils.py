import numpy as np 
# ADDME 
# Description: Module which contains all relevent ILP
#              functions. 
#                     (1) ILP()  
########################################################## 


########################################################## 
# Description:
#       Function to create the objective function.
#       Due to the size of the obj function, it will
#       be constructed in parts, each part representing
#       the sum terms.
# Inputs:
#        R   :: The request matrix
#        D   :: The total number of destinations
#        K   :: The total number of nodes
#        M   :: The total number of nodes
#        L   :: Set of vNF,
#        F   :: Set containing the functions
#        Sr  :: Set of starting nodes of each chain 
#        u   :: vecotr of vNF typ i requirements 
# Return:
#      obj   :: The composition of each summation term
#               in the objective function.
########################################################## 
def makeOBJ(K,L,R,P,V,C,Dk,Sr,rho): 
    debug = 0  

    #Get the size of the request
    row,col = R.shape 
    S = len(Sr)
    M = K;
    D = len(Dk)
    Ln= L              # The final value of L

    # Allocate vector size
    f1=np.zeros((K,L))
    f2=np.zeros((row,S,D,K,L))
    f3=np.zeros((row,S,D,K,M,L,L,L-1))
    f4=np.zeros((row,S,D,K,L))

    # The first term
    for kk in range(0,K-1):
        for ii in range(0,L-1):
            f1[kk,ii] = C[kk,ii]
    #END FOR(1) 

    print f1 

    # Second term
    for rr in range(0,row-1): 
        for ss in range(0,S):
            for dd in range(0,D): 
                for kk in range(0,K-1):
                    for ii in range(0,L-1): 
                        f2[rr,ss,dd,kk,ii]=rho[dd]*P[ss,kk]*V[rr,ii,1]
    # END FOR (2) 
    
    print len(f2.flatten())
    

    # Third term
    for rr in range(0,row-1):
        for ss in range(0,S-1): 
            for dd in range(0,D-1):
                for kk in range(0,K-1):
                    for mm in range(0,M-1):
                        for ii in range(0,L-1): 
                            for jj in range(0,L-1):
                                for ll in range(0,L-2):
                                    f3[rr,ss,dd,kk,mm,ii,jj,ll]=rho[dd]*P[kk,mm]*V[rr,ii,ll]*V[rr,ii,ll+1]
    # END FOR (3) 

    # Fourth term
    for rr in range(0,row-1): 
        for ss in range(0,S-1): 
            for dd in range(0,D-1): 
                for kk in range(0,K-1):
                    for ii in range(0,L-1):
                        #f4[rr,ss,dd,kk,ii]=rho[dd]*P[ss,kk]*V[rr,ii,Ln] 
                        print
    # END FOR (4) 
                        
    # Flatten all the all of the vectors and put into a single vector                         
    obj = np.hstack((f1.flatten(),f2.flatten(),f3.flatten(),f4.flatten()))

    if(debug): 
        print "In makeObjective:"
        print "Length: ", len(obj)
    
    
    return obj , f1.flatten(),f2.flatten(), f3.flatten(), f4.flatten()  