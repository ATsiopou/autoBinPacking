#! /usr/bin/env python
import os.path 
import loadData
import numpy as np 
import dijkstra as dkstra 
import hrUtils as utl 
import objUtils as ob 
import monteCarlo as mc 
# ADDME
# Description: This is the main driver program. The
#              The program is designed to solve the
#              location and chaining and chacheing
#              problem. Using Integer linear program 
#              using: 
#                     (1) ILP() 
#                     (2) Heuristic()           
# Inputs:
#              Inputs initially defined here and feed
#              the ILP() and Heuristic() as parameters.
#              The results are returned here and used
#              to display the optimal found with ILP
#              to Heuristic(). 
#
# Terms :
#        K :: Total number of nodes
#        F :: The set containing ALL vnf's 
#        R :: Request matrix. Each row is sngl request
#             whos order is preserved
#        C :: Cost for 
#        U :: Uitlization capacity of node k
#        L :: The NUMBER of vnf  TYPES 
#        F :: The set containing all vnf's 
#        u :: CPU core requirement for vNFi
#        b :: RAM memory requirement for vNFi      
#########################################################
os.system('clear')

eqlSymLength=20

# -- start Testing: loadData.PY module 
print 
print "="*eqlSymLength,  " [(START) : loadData.py  ]", "="*eqlSymLength
G,R,U,K,L,M,c,u,Sr,D,nAR,nMC = loadData.load(int(loadData.prompter())) 
print "="*eqlSymLength, " [(END) : loadData.py  ]", "="*eqlSymLength
print 

# -- end Testing: loadData.PY module 
# -- 
# -- 
# -- start Testing : objUtils.py
print 
print "="*eqlSymLength,  " [(START) : objUtils.py  ]", "="*eqlSymLength
# Here we are testing functions inside objUtils.py module 
r0 = 0
obj,f1,f2,f3,f4 = ob.makeOBJ(K,L,R,utl.makeP(G),utl.makeV(R,L), utl.makeC(K,L),D,Sr,utl.makeRho(D,r0) ) 
print 
print "="*eqlSymLength, " [(END) : objUtils..py  ]", "="*eqlSymLength
print 

# -- end Testing: objUtils.PY module 
# -- 
# -- 
# -- start Testing : dijstra.PY module 
print "="*eqlSymLength, " [(START) : dijkstra.py  ]", "="*eqlSymLength
#testing imported files 
print
print "[( Testing ) imported files ]" 
print "" 
print "[( Testing ) shortestPath(G,1,2) ]" 
print dkstra.shortestPath(G,'1','2')
# shortest path 
print 
print "[( Testing ) shortestPathMatrix(G) ]" 
P = dkstra.shortestPathMatrix(G) 
print P 

# --
# -
# --

# Testing random grpah  
print
print "[( Testing ) random graph creation ]" 
# Generate a random graph 4x3 
print 
print "[( Testing ) genGraph(K,nAR) ]" 
# Change the name of generatemultilatyergrpah ---- > wrapper : genGraph() to call it insead 
graph=dkstra.generateMultiLayerGraph(4,3)
print graph 
# Shortest path
print 
print "[( Testing ) shortestPathMatrix( genGraph(4,3)) ]" 
P = dkstra.shortestPathMatrix(graph) 
print P 
print 
print "="*eqlSymLength , " [(END) : dijkstra.py  ]", "="*eqlSymLength

# -- end Testing: dijkstra.PY module 
# -- 
# -- 
# -- start Testing : hrUtils.PY module 

print "="*eqlSymLength, " [(START) : hrUtils.py  ]", "="*eqlSymLength
# V 
print
print "[( Testing ) makeV(R,L) ]" 
V = utl.makeV(R,L) 
print V 
# -- start: Dijktra module wrappers in hUtils.py 
print
print "[( Testing hUtils.py ) : wrapper functions  ]"
# P wrapper in utlis
print
print "[( Testing ) makeP(G) ]" 
print utl.makeP(G) 
# getpath wrapper 
print
print "[( Testing ) getPath(G,srce,dest) ]" 
print utl.getPath(G,1,3) 
# -- end: Dijktra module wrappers in hUtils.py 
# R 
print
print "[( Testing ) makeR(numRequest) ]" 
print "nmber of req:" , 5 
print utl.makeR(5) 
# C 
print
print "[( Testing )  C ]"
print utl.makeC(K,L) 
# U/u
print 
print "[( Testing ) makeU  ]" 
U,u=utl.makeU(K)
print "[( Testing ) U  ]" 
print "Dimension of U : " , np.shape(U)  
print U 
print "[( Testing ) u  ]" 
print "Dimension of u : " , np.shape(u)  
print u 
print 
print "[( Testing ) makeD ]" 
D = utl.makeD(K,nAR) 
print "D" , D 
print
print "[( Testing ) chooseO(D) ]" 
nD,o = utl.chooseO(D) 
print "o" , o 
print "D" , nD 
print 
print "[( Testing ) makeRho(D,1) -- r0 for now is set to 1 ]" 
r0 = 0
ro = utl.makeRho(D,r0) 
print "ro:  ", ro
print 
print 
print "[( Testing ) getRandomAR() ]" 
print utl.getRandomAR() 
print 
print 

print "="*eqlSymLength, " [(END) : hrUtils.py  ]", "="*eqlSymLength
print 
# -- end Testing: Dijktra module wrappers in hUtils.py 
# -- 
# -- start Testing: monetCarlo.PY module 
print "="*eqlSymLength, " [(START) : monteCarlo.py  ]", "="*eqlSymLength
# -  PPCC  - #
print
print "\t\t[( Testing ) case 1 : PPCC / STATICPPCC / SPBL (NAIVE)  ]" 
print "\t\t","="*eqlSymLength, "\tK\t", "="*eqlSymLength
mc.monteCarlo('K',100,Sr,L,V,f1,f2,f3,f4) 
print 
# -    - #
print 
print "\t\t[( Testing ) case 2 : PPCC / STATICPPCC / SPBL (NAIVE)   ]" 
print "\t\t","="*eqlSymLength, "\tR\t", "="*eqlSymLength
print 

# -  PPCC  - #
print 
print "\t\t[( Testing ) case 3 : PPCC / STATICPPCC / SPBL (NAIVE)  ]" 
print "\t\t","="*eqlSymLength, "\tRho\t", "="*eqlSymLength
print 



print "="*eqlSymLength," [(END) : monteCarlo.py  ]", "="*eqlSymLength


# -- end Testing: monetCarlo.PY module 
# -- 
# -- start Testing: PPCC.PY module 












