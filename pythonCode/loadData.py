import numpy as np 
import os
# ADDME
# Description: Loads data, prompt usr for type ret data 
# Inputs     : NONE 
# Return     :
#       nAr :: Number of access routers for graph  
#       G   :: Graph to be returned 
#       R   :: The request matrix 
#       C   :: The node cost matrix 
#       K   :: The total number of nodes 
#       M   :: The total number of nodes 
#       L   :: Set of vNF 
#       U   :: Node utility constraints  
#       u   :: vNF utility requirements 
#########################################################


#########################################################
# Descr : Prompt function 
#
#########################################################
def prompter():
    print 'Options:' 
    print '1) K = 6  , L = 5, R = 5 ' 
    print '2) Monte Carlo Simulation ' 
    # prompt 
    var = raw_input("Enter an option:  ")
    return var 
######################################################### 
#Descr : 
#
#
######################################################### 
def load(choice):
    if choice == 1 : 

        with open('configFiles/conf1/G.conf') as fileG : 
            G = np.loadtxt(fileG)
        with open('configFiles/conf1/R.conf') as fileR : 
            R = np.loadtxt(fileR) 
        with open('configFiles/conf1/c0.conf') as filec : 
            c = np.loadtxt(filec)
        with open('configFiles/conf1/U.conf') as fileU : 
            U = np.loadtxt(fileU) 
        with open('configFiles/conf1/u.conf') as fileu : 
            u = np.loadtxt(fileu)
        with open('configFiles/conf1/Sr.conf') as fileSr : 
            Sr = np.loadtxt(fileSr) 
        with open('configFiles/conf1/D.conf') as fileD : 
            D = np.loadtxt(fileD)
        # The number of access routers
        nAR = 3             
        L = 5 
        numMCarlo = 0 
    elif choice == 2 :
        print "Choice 2"
        with open('configFiles/conf2/G.conf') as fileG : 
            G = np.loadtxt(fileG)
        with open('configFiles/conf2/R.conf') as fileR : 
            R = np.loadtxt(fileR) 
        with open('configFiles/conf2/c0.conf') as filec : 
            c = np.loadtxt(filec)
        with open('configFiles/conf2/U.conf') as fileU : 
            U = np.loadtxt(fileU) 
        with open('configFiles/conf2/u.conf') as fileu : 
            u = np.loadtxt(fileu)
        with open('configFiles/conf2/Sr.conf') as fileSr : 
            Sr = np.loadtxt(fileSr) 
        with open('configFiles/conf2/D.conf') as fileD : 
            D = np.loadtxt(fileD)        
        # The number of access routers
        nAR = 5             
        L = 0         
        # receive the total number of MC iterations 
        numMCarlo = raw_input("Number of Iteration:  ")
    else:
        print "Not a valid choice"
        
    # Get the number of nodes, shape returns row,col = somethin.shape 
    row = G.shape; 
    K = row[1] - nAR;  
    M = K;         
    
    os.system('clear') 
    return G,R,U,K,L,M,c,u,Sr,D,nAR,numMCarlo    

######################################################### 
# Descr :  make the shortest path matrix 
#
#
######################################################### 
def makePaths(G):    
    # For k (olumns) in all collumns 
    n = G.shape[1]
    print n
    P = np.zeros((n,n))
    print P 
    for k in range(0,n): 
        for m in range(0,n): 
            if k == m: 
                P[k,m] = 0 
            cost,path = dijkstra(G,k,m)
            P[k,m] = cost
    return P
######################################################### 
# Description:
#       Creates the V ( former phi ) matrix. The matrix 
#       tells us if the lth request of r, vNF type i
# Inputs:
#        R   :: Number of access routers for graph  
#        L   :: Graph to be returned  
# Return : 
#       V   :: (request)x(type_i)x(lth_function) matrix.  
######################################################### 
def makeV(R,L):
    rows,cols = R.shape
    V = np.zeros((L,L,rows))
    for i in range(0,rows): 
        for j in range(0,cols):
            r = R[i,j]       # Extract the request value 
            V[i,j,r-1] = 1   # rows(rqst r ) col (vnf) reqstd r (indicates request)  
    # end for(s) 
    return V


    
    





