import numpy as np 
import os 
import dijkstra as dkstra  
import random as rndm 

# ADDME 
# DESCR : 
#         Heuristic utility functions. 
#         Module contains shared functions of the heuristics       
#         used in Monte carlo simulation. 
# USE   :
#         import module at top for python pre-process, giving 
#         access to files below.   
# Expl :  
#         import hrUtils as utl 
#          ... 
#         utl.getPath(G,start,end)  
##############################################################

##########################################################
# DSCR   : 
#          Get the path of given source and destination 
#          node.   
# INPUT  :        
#  G    :: 
# source:: start node  
# dest  :: end node 
# RTN   :        
#  p    ::  3-tupe (cost,stringPath,intPath) 
##########################################################
def getPath(G,source,destination):
    return dkstra.shortestPath(G,source,destination) 
##########################################################
# Func     : wMakeR
# Decr     : Make request wrapper function. Loop over the
#            number of requests (rows) and use randperm
#            to gen. rand nums from 1-4 of vecSize.
# Input    :
# numReq  :: Random number of requests - number of rows.
#Local Vars:
# minInt  :: min bound
#vecSize  :: The size of the vector
# numInts :: The number of ints to return
# Return   :
#     R   :: Request matrix
##########################################################
def makeR(numReq):
    vecSize = 3  # Size of each individual request 
    maxInt = 5   # The maximum allowable integer in the array 
    minInt = 1 
    # Create an empty array with the right dimensionality 
    R = np.empty((0,vecSize), int)
    
    # Iterate over the number of requests , adding each one to the top 
    for r in xrange(numReq):
        row = rndm.sample(range(minInt, maxInt), vecSize)
        R   = np.row_stack((R, row))
    return R  
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
            V[i,j,r-1] = 1   # rows(rqst r ) col (vnf) requested r (indicates request)  
    # end for(s) 
    return V
##########################################################
# DSCR  : make the shortest path matrix. 
#         This just calls imported dkstra modules 
#         shortestPAthMatrix(G) function. Here as a 
#         as a quick and dirty hack 
# INPUT :        
#   G  :: Graph in matrix form  
# RTN   :        
#   P  :: Shortest path matrix P from graph G  
##########################################################
def makeP(G):    
    return dkstra.shortestPathMatrix(G) 
##########################################################
# Func     : wMakeC
# Decr     : Make C matrix wrapper function.
# Input    :
#     K   :: Number of nodes
#     L   :: number of vNF
# Return   :
#     C   :: Cost Matrix
##########################################################
def makeC(K,L):
    return np.zeros((K,L))
##########################################################
# Func     : wMakeUu
# Decr     : Make V matrix wrapper function.
# Input    :
#     K   :: Number of nodes
#     L   :: number of vNF
# Return   :
##########################################################
def makeU(K):
    # create U as an 2x1 array 
    valU = np.array([[2000],[30]])    
    # Here we make u. 
    # first identify the rows of u 
    valu1 = [40 , 10 , 20 ,30] 
    valu2 = [ 1 , 1 , .5 , .5 ]  
    # stack  u together 
    u = np.vstack([valu1,valu2])
    # U should be returned as a 2xK matrix 
    U = np.tile(valU,(1,K))
    return U,u



# -- End of module 





























##########################################################
# DSCR  : 
#          
# INPUT :        
#      :: 
#      :: 
#      :: 
# RTN   :        
#      :: 
##########################################################

