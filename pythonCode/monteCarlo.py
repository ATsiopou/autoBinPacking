import dijksta as dk
import numpy as np


##########################################################
# DSCR
#         Init function for monte carlo script 
# INPUT
#    c :: Choice, inidicating the choice of simulation type 
# RTN
#      :: 
##########################################################
def monteCarlo(choice):

    if ( choice == 'K' ):
    # This simulates monte carlo for nodes K
        # RUN mcarloK
        # retrun : [mPPCC,mNaive,msPPCC]
        monteCarlo() 

    elif ( chcice == 2 ):
    # Simulate monte carlo for Requeasts
        # RUN mcarloP
        # retrun : [mPPCC,mNaive,msPPCC]
    elif( choice == 3 ):
    # Simulate Rho change in monte Carlo
        # RUN mcarloRHO
        # retrun : [mPPCC,mNaive,msPPCC]
    else:
        return 0




###########################################################
# DESCR
#         prints the average gains of monte carlo type 
#         [type] of each heuristic. 
# INPUT 
#  d1  :: Data vector of the 1st sim, containing avrg res
#  d2  :: Data vector of the 2nd sim, containing avrg res
#  d3  :: Data vector of the 3rd sim, containing avrg res
#  d4  :: Data vector of the 4th sim, containing avrg res
###########################################################
def printAverageGains(d1,d2,d3,mcSimulation):
    print "----------------------------------------" 
    print " PPCC v.s. AGW : " , calcAverageGains(d1,d2)
    print " PPCC v.s. SPBA: " , calcAverageGains(d1,d3)
    print " SPBA v.s. AGW : " , calcAverageGains(d3,d2)
    print "----------------------------------------" 
###########################################################
# DESCR
#         Calculate the average perentage increase 
#         
# INPUT 
#  d1  :: Data vector of the 1st sim, containing avrg res
#  d2  :: Data vector of the 2nd sim, containing avrg res
# RTN
# avrg :: Data vector containing results 
###########################################################    
def calculateGains(d1,d2):
    a = calculateAverage(d2)
    b = calculateAverage(d1) 
    gain = (abs(a-b)/a)*100 
    return gain
###########################################################
# DESCR
#         Calculate avergae of a vector 
# INPUT 
#  d   :: Data vector of the 1st sim, containing avrg res
# RTN
# avrg :: calculated average of the returned data  
###########################################################    
def calculateAverage(d):
    n1 = len(d)
    avrg = (sum(d)/n1)
    return avrg 

###########################################################    
# Func     : printRound()
# Decr     : print the round function
# Input    :
# numNodes :: number of nodes
# numReq   :: Number of requests (num of rows in R)
#     mP   :: ppcc mean solution vector of curr. round
#     mN   :: Naive mean solution vector of curr. round
# Return   : NONE
###########################################################    
def printRound(numNodes,numRequest,rhoVal,mP,mN,mS,mcSimulation):
    print "-"*15
    print "-\t\t[" ,mcSimulation ,"]\t\t-" 
    print "-"*15 
    print "Request Size\t:"  , numRequest 
    print "Topology Size\t:" , numNodes 
    print "Rho\t\t:"         , rhoVal  
    print "Mean AGW\t:"      , mN  
    print "Mean SPBA\t:"     , mS  
    print "Mean PPCC\t:"     , mP




