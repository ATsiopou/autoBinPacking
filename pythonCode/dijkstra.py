import numpy as np 
import random as rndm
import decimal 
import math 
from numpy.linalg import norm
import scipy.sparse
from graphviz import Digraph
from graphviz import Source
from subprocess import call
from priodict import priorityDictionary
from PIL import Image   # To print image after saving 
# ADDME 
# DESCR : 
#         Dijkstra Algorithm
#         Find shortest paths from the start vertex to all
#         vertices nearer than or equal to the end.
# INPUT : 
#   G  :: Dictionary indexed by verticies 
#         For any         v, G[v] is itself a dictionary. 
#         For any edge v->w, G[v][w] is the length/cost of 
#                            the edge 
#         G/G[v] are not dictionary python objects, but can 
#         be any object that obeys the ordering. 
#       + Example: 
#         for instance a wrapper in which vertices are URLs
#         and a call to G[v] loads the web page and finds 
#         its links.
#    s :: Source node 
#    d :: destination node  
#
# RTN   : 
# D[v] :: Distance/cost from start to node v 
# P[v] :: Predicessor to v along the shortest path from s to v  
# (D,P):: The return tuple 
# 
# USE   :
# [cost rute] = dijkstra(Graph, source, destination)
#  
# Example :  
# G = [0 3 9 0 0 0 0;
#       0 0 0 7 1 0 0;
#       0 2 0 7 0 0 0;
#       0 0 0 0 0 2 8;
#       0 0 4 5 0 9 0;
#       0 0 0 0 0 0 4;
#       0 0 0 0 0 0 0;
#       ];
#  
##############################################################
def dijkstra(G,start,end=None):
    D = {}  # dictionary of final distances
    P = {}  # dictionary of predecessors 
    Q = priorityDictionary()   # est.dist. of non-final vert.                      
    Q[start] = 0

    for v in Q:
        D[v] = Q[v]
        if v == end: break
        for w in G[v]:            
            vwLength = D[v] + G[v][w]
            if w in D:
                if vwLength < D[w]:
                    raise ValueError, \
    "Dijkstra: found better path to already-final vertex"
            elif w not in Q or vwLength < Q[w]:
                Q[w] = vwLength
                P[w] = v
    return (D,P)
##########################################################
# DSCR    : 
#           Find the single shortest path 
# INPUT   :        
#    G   :: The original graph as an numpy nd array 
#  start :: Starting vertex   
#   end  :: End 
#OUTPUT   :
#    D   :: D[v] is the distance (cost) from start to v 
#    P   :: Predecessor of v along the shortest path 
#           from start to v 
# RTN    :        
# string
#   Path :: List of nodes (string ) on shortest path 
#           from start to v 
# int 
#   Path :: List of nodes (int) on shortest path from  
#           start to v
#      D :: Integer cost to get to the final vertex 
##########################################################
def shortestPath(G,start,end):
    # debug for error reporting 
    # flag1/2 used to indicate if keys start.end in dictionary 
    debug=0      
    flag1=0
    flag2=0

    # debug output 
    if (debug):
        print "[(shortestPath) DEBUG ]"
        print "Checking matrix: "
        print G 
        print "Checking existance of path :" , start, " ---> ", end
    
    # If G is a matrix, convert it to dictionary 
    if type(G).__module__ == 'numpy' :
        start = str(start) 
        end = str(end) 
        G = matToDic(G)
        #print G 
    # Check to see if the start and end values are in the dictionary 
    if start in G.keys():         
        flag1 = 1
    if end in G.keys(): 
        flag2 = 1
    if (flag1 == 1) and (flag2 == 1) : 
        D,P = dijkstra(G,start,end)
        if ( debug ) :
            print "[(shortestPath) DEBUG ]"
            print "D : " , D 
            print "P : " , P        
            
        # Check if end is in the path P 
        if end not in P.keys(): 
            if ( debug ) :
                print "[(shortestPath) DEBUG ]"
                print "[(shortestPath) Error: ] No Path exists ...  " 
            return 0,0,0
    else:
        return 0,0,0

    # Extract the cost and revers the path                                        
    stringPath = []
    
    # There is a key error here which arises when there is a path, but that path is only a partial path.
    # Fix: before going into this loop, check if there the key : "end" exists in the returned path
    #      exists ) continue 
    # doesNotExist) return a three-tuple (0,0,0)      
    while 1:
        stringPath.append(end)
        if end == start: break
        end = P[end]
    stringPath.reverse()

    # Extract the cost and path                                       
    Cost = D[stringPath[-1]]
    # Convert the path to array of ints 
    intPath = map(int, stringPath) 
    
    if ( debug ) :
        print "Cost: ", Cost 
        print "Path: ", stringPath 

    return Cost, stringPath ,intPath 
##########################################################
# DSCR  : 
#         Create sortest path matrix P  
# INPUT :        
#  G   :: The original graph 
# RTN   :        
#  P   :: A shortest path matrix based on G 
##########################################################
def shortestPathMatrix(G):
    debug = 0 
    
    if(debug):
        print "SHORTEST PATH MATRIX" 
        # check the type 
        if type(G).__module__ == 'numpy' :
            print "[G TYPE: ] matrix "
        else:
            print "[G TYPE: ] dictionary "
            
    # Copy to local temp matrix      
    tempG = np.copy(G)
    n = tempG.shape[0]
    P = np.zeros((n,n))
    # Fill the matrix with S.P. val is it exists 
    for k in range(0,n):
        for m in range(0,n):
            cost,path,ipath = shortestPath(G,k+1,m+1)
            P[k,m] = cost
    return P
##########################################################
# DSCR   : generateMultiLayerGraph() 
#         Create a random graph G 
# INPUT         
#   K  ::  Number of nodes 
#  nAR ::  number of Access routers 
# RTN
#    G :: The original graph            
##########################################################
def generateMultiLayerGraph(K, numOfAccessRouters): 
    
    # Get dimensions, create a graph G with dim 
    n = K+numOfAccessRouters 
    G = np.zeros((n,n)) 

    # Construct the first part of the graph 
    layerA = createLayer('A',G,K,numOfAccessRouters)  
    
    # Identify the dimensions for inter-node-commute layerB  
    numberInLayerA = layerA.shape[0]      
    numberInLayerB = K - numberInLayerA
    
    # Create the third layer => Connecting GW to internal nodes 
    createLayer('B',G,K,numOfAccessRouters)
    
    # Create the third layer => Connections to Access Routers 
    createLayer('C',G,K,numOfAccessRouters) 

    # reclaim the full matrix 
    G = G + np.transpose(G)                  
    return G 
    


##########################################################
# DSCR   : createLayer() 
#         Create a random graph G 
# INPUT         
#   K  ::  Number of nodes 
# RTN
#    G :: The original graph in matrix form             
##########################################################
def createLayer(case,G,K,nAR): 
    if (case == 'A'):     
        # Get the dimension 
        aXDim = G.shape[1] 
        
        # Begin the loop, get a random number 
        i = 1 
        startSeed = 1 
        while( i < aXDim-nAR): 
            if (G[0,i] == 0 ): 
                G[0,i] = np.ceil( rndm.random() * 100)  
            i=i+1         
        return G  
        # END CASE 1
    elif ( case == 'B' ) :

        #tmp = checkVal(tmp,bXDim,density)
        flag = 0 
        bXDim = (len(G) - nAR) - 1  # Get the dimension of B matrix  
        
        #while flag IS NOT TRUE, check that the graph is legitimate 
        while ( flag != 1 ): 
            tmp = np.zeros((bXDim,bXDim)) 
            density = rndm.uniform(0,1)
            tmp = scipy.sparse.rand(bXDim,bXDim,density)
            tmp = tmp.todense()                            # After above, fill it up  
            tmp = np.around(tmp,decimals=2)                # Sifting dance  
            tmp = np.ceil(tmp*5)                           # instead of np.ceil(A*10)->A*10/2
            tmp = np.triu(tmp,k=1) 
            tmp = tmp + np.transpose(tmp)                  # reclaim the full matrix 
            if ( ensureLinks(tmp) == 1 ):
                flag = 1        
        
        # find each non zero value and replace it with a ranint b/w 0 100 
        for i in range(len(tmp)) :
            for j in range(len(tmp)) : 
                if (tmp[i,j] != 0 ): 
                    tmp[i,j] = np.ceil( rndm.random() * 100)  
        
        #Combine temp into the larger matrix G
        G[1:bXDim+1,1:bXDim+1] = np.triu(tmp,k=1) 
        return G
        # END CASE 2
    elif ( case == 'C' ):    
        
        # Extract dim. and create tmp matrix 
        n = G.shape[0] 
        cYDim = n - nAR  # rows 
        cXDim = nAR      # cols 

        tmp = np.zeros((cYDim,cXDim)) 
        
        # Insert the values into the temp matrix 
        for k in range(0,cXDim): 
            randRow = rndm.randint(1,cYDim-1) 
            tmp[randRow,k] = np.ceil(rndm.random()*100) 
        
        # Insert the temp matrix into Graph matrix 
        G[0:n-nAR:,nAR+1:] = tmp 
        # END CASE 3 
    return 0              
##########################################################
# Func     : ensureLinks()
# Decr     : Verifies that there is a link from the
#            source node to the destinations nodes.
# Input   :
#      K  :: The number of nodes for the graph
#      G  :: The graph G to be returned
#   n_AR  :: The number of access routers
# Return   :
#      b  :: Bool, true/false
##########################################################
def ensureLinks(G):
    debug = 0 
    b = 1
    m,n= G.shape

    # Make sure that G is not == 0, if it is, gen another matrix 
    if ( np.count_nonzero(G) == 0 ): 
        if ( debug ): 
            print "Matrix was all zeros ... generating a new random matrix " 
        b = 0
        return b

    # Iterate over the matrix and look for a paths 
    for e in range(0,m):
        for d in range(0,n):
            if (e != d):
                # Adding the +1 to align the matrix index and dict 
                pCost,sPath,iPath=shortestPath(G,e+1,d+1) 
                if (iPath == 0):
                    if(debug):
                        print "----------------------------"
                        print "Failure: Check ensureLinks()"
                        print "Cost: ", pCost 
                        print "Path: ", sPath 
                        print "----------------------------"
                    b = 0
    return b
##########################################################
# DSCR   
#         Get a random value between integers start and 
#         end 
# INPUT         
# start:: Lower limit to value range 
#  end :: the upper lim of value range 
# RTN          
#  val :: random integer value 
##########################################################
def getRandVal(start,end): 
    return rndm.randint(start+1,end+start+1) + rndm.randint(0,3)     
##########################################################
# DSCR   
#         Create a dictionary from the 2-D matrix G 
#         node start -> end. 
# INPUT         
#    G :: The original graph 
# RTN          
# gDic :: Dictinary  
##########################################################
def matToDic(G):
    # Start i = i+1 to index nodes starting at 1                             
    keys = [str(i) for i in xrange(len(G))]
    D = {}
    # Loop over the numpy matrix and add to D set                                       
    for r in xrange(len(G)):
        for c in xrange(len(G)):
            if G[r,c] != 0:
                D.setdefault(str(r+1),{}).update({str(c+1) : int(G[r,c])})
    return D
##########################################################
# DSCR   
#         Create a matrix from the dictionary G 
# INPUT         
#    D :: Dictinary      
# RTN
#    G :: The original graph            
##########################################################
def dicToMat(D):
    # Get the number of keys
    # Create a first row/col of zeros, add 1 then remove the padding to 
    # regain a matrix of size nxn 
    n = len(D.keys())+1
    # Now, Create the numpy array
    G = np.zeros((n,n))
    # Loop over the numpy matrix and add to gDic set                                  
    for key1, row in D.iteritems():
        for key2, value in row.iteritems():
            #print "k1",key1, "k2:" , key2 ,"val", value  
            G[int(key1), int(key2)] = value
            
    G = np.delete(G,0,0)          # remove row 0 (first row) 
    G = np.delete(G,np.s_[0],1)   # remove col 0 (first col)
    return G
##########################################################
# DSCR   
#        Print the graph.  
# INPUT         
#      G  :: Dictionary NOT MATRIX (YET)  
# Input    :
#      K  :: The number of core nodes for the graph
#     nAR :: The number of Access Routers 
##########################################################
def printGraph(G):     
    pngName = "top.png" 
    f = open('top.dot','w')
    f.writelines('digraph G {\nnode [width=.3,height=.3,shape=circle,style=filled,color="black",fillcolor=white,fontcolor=firebrick4] \nedge [penwidth=0.75] \noverlap="false";\rrankdir=LR;\n')
    f.writelines
    for i in G:
        for j in G[i]:
            s= '      '+ i
            s +=  ' -> ' +  j + ' [label="' + str(G[i][j]) + '"]'
            s+=';\n'
            f.writelines(s)
    f.writelines('}')
    f.close()
    call(["neato","-Gstart=9","-Tpng","top.dot", "-o", pngName]);
    
    # With PIL 
    img = Image.open(pngName) 
    img.show()

    print "Graph saved .. "    




