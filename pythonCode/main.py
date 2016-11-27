#! /usr/bin/env python
import os.path 
import loadData
import dijkstra as dkstra 
import hrUtils as utl 
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
# Cast prompter return value as an int, to be processed by load.
G,R,U,K,L,M,c,u,Sr,D,nAR,nMC = loadData.load(int(loadData.prompter())) 
# Test printGraph 
#dkstra.printGraph(dkstra.matToDic(G))


#dkstra.shortestPath(G2,'1','2')
# Create the shortest path matrix 
#print dkstra.shortestPath(G,'1','3')

# Testing Dijkstra.PY 
# --------- start dijkstra testing 
graph = dkstra.generateMultiLayerGraph(4,3)
print "MAIN.PY: GRAPH TYPE:  " , type(graph) 
P = dkstra.shortestPathMatrix(graph) 
#Take the original graph 
P = dkstra.shortestPathMatrix(G) 
print P 

# --------- end dijkstra testing 



# Testing Heuristic Utils .PY 

# Testing MontCarlo.PY 










