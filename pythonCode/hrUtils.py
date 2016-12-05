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
##########################################################
# DSCR  : 
#         Make destination vector based on number of
#         access routers     
# INPUT :        
# nAR  :: Number of access routers 
# RTN   :        
# D   :: Vector containing destination nodes. 
##########################################################
def makeD(K,nAR):
    # Create a 1xnAR vector D 
    D = np.zeros((nAR))
    totalD = K+nAR
    count = 0
    start = K+1; 
    # Insert d (the access router index) inside D vecter 
    for d in range(start,totalD+1):
        D[count] = d
        count = count + 1 
    # The vector now contains the indexes of nAR ar's 
    return D 
##########################################################
# DSCR  : 
#          Choose a starting destination node given
#          a set of destinations.
# INPUT :
#   D  :: vector of destination nodes 
# RTN   :        
#   o  :: The starting destination for cache 
#   D  :: The revised vector, missing destination o
##########################################################
def chooseO(D): 
    # Choose a random number from group of available AR's
    #- set this value, which is in vector D to o
    numm = len(D)
    rNum = rndm.randint(0,numm-1)       
    o = D[rNum]
    # recreate the vector, NOT including the ones in excluded set 
    excludeIndex = {rNum}
    D = [elm for i,elm in enumerate(D) if i not in excludeIndex ]
    return D,o
##########################################################
# DSCR  : 
#         Create a prob. vector rho. Choose a random
#         number bw 0 / 100 and return it in ro.
# INPUT :        
#   Dk :: vector of destination nodes 
#   r0 :: The initial rho probability 
# RTN   :        
#   ro :: prob vector, indicating prob of mobility. 
##########################################################
def makeRho(Dk,r0):
    # Deifne local variables 
    nDestNodes = len(Dk)
    ro   = np.zeros((nDestNodes))
    temp = np.zeros((nDestNodes))
    # Ceck, is initial condition the same as max prob
    if(r0 == 100 ):
        ro[0] = 1
        for dd in range(1,nDestNodes):
            ro[dd] = 0
    else:
        maxVal = 100;
        ro[0] = r0 / 100;
        temp[0] = 0;
        # aa should contain [len(D)-1] # of elmnts from [1-(maxVal-r0)] 
        aa = np.random.randint(1,maxVal-r0,len(Dk)-2)
        # Sort the vector, then assign from +1 beyond first index and -1 from last
        temp[1:nDestNodes-1] = np.sort(aa,axis=None)
        # Give the last element the differemce 
        temp[nDestNodes-1] = maxVal - r0
        # iterate over and normailze 
        for dd in range(1,len(Dk)):
            ro[dd] = (temp[dd] - temp[dd - 1]) /100            
    return ro 
##########################################################
# DSCR   : 
#          Get a random number through 1-5 of AR
# INPUT  : NONE
# RTN    :        
#   num :: Random number to return
# LOCAL  : 
# minInt:: lower bound   [  INCLUSIVE  ]   
# maxInt:: upper bound   [  EXCLUSIVE  ]   
# numInt:: The number of ints to return
##########################################################
def getRandomAR(): 
    minInt  = 1  
    maxInt  = 6
    numInts = 1
    return np.random.randint(minInt,maxInt,size=numInts)
##########################################################
# DSCR   : 
#          Initialize the maps and essential components
#          of algorithm ppcc/staticPPCC/naive 
# INPUT  : NONE
# RTN    :
# Return  :
# fAllocationTable:: Contains the k,l,r map combo, plus
#                   two additional cols indicating where
#                    it failed
# alloctionTable  :: Set size of table. Holds node,func
#                    request mapping
#  ROW  :: K
#  COL  :: L
#  AGE  :: r
#---------------
#               R :: service request
#             r,c :: Number of rows/col of Request matrix
#               x :: x allocation vector
#              RU :: Remaining utility
#               x :: x allocation vector
#              f1 :: x_k_i of objective functions
##########################################################
def init(R,K,L,U,f1):
    r,c    = R.shape 
    #xfinal = zeros(1,length(f1(:)'))
    xFinal = np.zeros((1,len( f1.flatten() ))) 
    xTable = np.zeros((K,L))
    RU     = np.zeros((U.shape))
    RU     = U
    allocationTable = np.zeros((K,L,r))
    fAllocationTable = np.zeros((K,L,r))        
    pcCost = 0

    global fAllocationTable
    global allocationTable
    global xTable
    global xFinal
    
    return fAllocationTable,allocationTable,xTable,pcCost,RU,xFinal,r,c
##########################################################
# Func    : printSummary()
# Decr    : Prints hosting either
#           1) successfull
#           2) failed
#           3) reason h/u
# fAllocationTable:: Contains the k,l,r map combo, plus
#                    two additional cols indicating where
#                    it failed
# alloctionTable  :: Set size of table. Holds node,func
#                    request mapping
##########################################################
def printSummary():
    print " STUB " 
##########################################################
# Func    : getNodeFromFunc() 
# Decr    : Return the node for function f was mapped
#           to. Plot function utility.
##########################################################
def getNodeFromFunc(func,req,K,allocationTable): 
    node  = 1
    counter = 1
    for kInd in range(0,K):
        if( allocationTable[kInd,func,req] == 1 ):
            node = counter
        counter = counter + 1
    return node
##########################################################
# Func    : getDestinationNode()
# Decr    : Given the destination set D, the prob.
#           vector rho,clc. the corresponding
#           destination node.
# Return  :
#   node :: Node corresponding to max rho index in set D    
##########################################################
def getStaticDestinationNode(o):
    # find the max val
    node = o
    return node                     
########################################################
# Func    : getPpccDestinationNode()
# Decr    : Given the destination set D, the prob.
#           vector rho,clc. the corresponding
#           destination node.
# Return  :
#   node :: Node corresponding to max rho index in set D
########################################################
def getPpccDestinationNode(D,rho):
    # find the max val
    maxx = np.max(rho)
    node = 1
    count = 1
    
    for i in range(1-1, len(rho)-1):
        if(maxx == rho[i]):
            node = D[i]
        count = count + 1
    return node
########################################################
# Func    : getPath()
# Decr    : Calculate the shortest path.
# Input:
#    G    :: The undirected graph
#    s    :: Source node
#    s    :: Destination node
# Rtn  :
#   cost  :: The cost of the path
#   path  :: The path elements
########################################################
def getPath(G,source,dest):
    # For each access router find two paths
    cost, sPath, iPath = dkstra.shortestPath(G,source,dest)
    return cost , iPath
########################################################
# Func     : getStarting Node
# Decr     : Calculate the starting node location with
#            with the minimum cost.
# Locl vars:
#   sNode :: The starting node
#   minVal:: The current minimum value
#   cost  :: Cost of the path
#   path  :: The path, in terms of its elem. nodes.
########################################################
def getStartNode(G,Sr,d):
    # Choose some (relatively large) min. value to start.
    minVal = 100; 
    pathCost = np.zeros((1, len(Sr)))
    start = int(Sr[0])
    end = len(Sr)-1 
    print "Start:", start 
    print "End  :", end  
    for ii in range(0, end):
        cst,path = getPath(G,ii,d)
        pathCost[ii] = cst
        if ( cst <= minVal ):
            minVal = cst
            print path
            startingNode= path
        # Reset the cost and paths
        path = 0
        cst  = 0
    return startingNode

########################################################
# Func    : getPath()
# Decr    : wrapper function for getPath()
# Input   :
#      s :: source
#      d :: destination
########################################################
def getCandidatePath(G,s,d):
    cost, sNodes = getPath(G,s,d)
    return sNodes
########################################################
# Func    : isHosted()
# Decr    : Evealuates if func is hosted at node for
#           service reqest r.
# Input   :
#   func :: virtual network function
#   node :: node k
# request:: service request.
#
# Return  :
#      b :: Bool, tf true:yes, false:no.
########################################################
def isHosted(node,func,request):
    if( allocationTable[node,func,request]):
        b = 1
    else:
        b = 0
    return b
########################################################
# Func    : host()
# Decr    : Set the bit in the allocationTable to 1.
#           Indicates a VNF has been placed on node for
#           request r.
# Input   :
#   func :: virtual network function
#   node :: node k
# request:: service request.
#     b  :: bit, 1/0
########################################################
def host(node,func,request,b):
    allocationTable[node,func,request] = b
########################################################
# Func    : setxTable()
# Decr    : Set the bit in the x vector map/table to 1.
#           Indicates a VNF has been placed on node for
#           agnostic to request.
# Input   :
#   func :: virtual network function
#   node :: node k
#    b   :: either bit to set 1/0
########################################################
def setxTable(node,func,b):
    xTable[node,func] = b
########################################################
# Func    : mapTicker
# Decr    : Records the mapping, and failurs
# Input   :
# request:: service request.
#   func :: virtual network function
#   node :: node k
#    b   :: either bit to set h/u
#      u :: indicates utility failure
#      h :: indicates function isHosted at node k
########################################################
def hostFail(node,func,request,b):
    fAllocationTable[node,func,request] = b
########################################################
# Func    : updateResources()
# Decr    : Update the resource vector U by decreasing
#           it by u for function func.
# Input   :
#   func :: virtual network function
#   node :: node k
#    U   :: Node utility
#    u   :: function requirement
########################################################
def updateResources(U,u,node,func):
    U[1,node] = U[1,node]-u[1,func]
    U[2,node] = U[2,node]-u[2,func]
    return U
########################################################
# Func    : canNodeProcess()
# Decr    : Check to see if node has resources to process
#           the current vNF in r
# Input   :
#   func :: virtual network function
#   node :: node k
#    U   :: Node utility
#    u   :: function requirement
#
# Return  : true: yes / false:no
########################################################
def canNodeProcess(U,u,node,func):
    if( (u[1,func] <= U[1,node]) and (u[2,func] <= U[2,node]) ):
        b = 1
    else:
        b = 0
    return b
########################################################
# Func    : getNode()
# Decr    : Return the node given the function,
#           and request
# Return  : Node
########################################################
def getNode(K, func, req, allocationTable):
    node = 1
    counter = 1
    for kInd in range(1-1, K-1):
        if ( allocationTable[kInd, func, req] == 1):
            node = counter
            
        counter = counter + 1
    return node


# -- End of module 
