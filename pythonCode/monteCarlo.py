import hrUtils as utl 
import dijkstra as dk
import numpy as np
##########################################################
# DSCR
#         Init function for monte carlo script 
# INPUT
#    c :: Choice, inidicating the choice of simulation type 
# RTN
#      :: 
##########################################################
def monteCarlo(simType,RUN,L,V,f1,f2,f3,f4):
    
    print simType
    
    if ( simType == 'K' ):
    # This simulates monte carlo for nodes K
        print "-"*20
        print "Monte Carlo simulation [K]"
        print "-"*20

        mPPCC,mNaive,msPPCC = monteCarloK(RUN,L,V,f1,f2,f3,f4,simType);
        #printAverageGains(mPPCC,mNaive,msPPCC,mcSimulation); 

    elif ( simType == 'R' ):
    # Simulate monte carlo for Requeasts
        print "-"*20
        print "Monte Carlo simulation [R]" 
        print "-"*20

        #mPPCC,mNaive,msPPCC = monteCarloR(RUN,L,V,f1,f2,f3,f4,simType);
        #printAverageGains(mPPCC,mNaive,msPPCC,simType); 

    elif( simType == 'Rho' ):
    # Simulate Rho change in monte Carlo
        # RUN mcarloRHO
        # retrun : [mPPCC,mNaive,msPPCC]
        print "-"*20
        print"Monte Carlo simulation [Rho]"
        print "-"*20
        
        #mPPCC,mNaive,msPPCC = monteCarloRho(RUN,L,V,f1,f2,f3,f4,simType);
        #printAverageGains(mPPCC,mNaive,msPPCC,simType); 

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

###########################################################    
# Func     : monteCarloK
# Decr     : Monte carlo simulation with a varying 
#             topology size. Everything else remains 
#             constant. 
# Input    :
#      K  :: The number of nodes for the graph
#      G  :: The graph G to be returned
#     nR  :: The number of access routers
# Return   :
#  mPPCC  :: monte c ppcc avrg sol vector for each k
#  mNaive :: monte c naive avrg sol vector for each k
###########################################################    
def monteCarloK(RUN,L,V,f1,f2,f3,f4,simType): 
    NUMBER_REQUESTS = 5
    K_START = 10
    K_END   = 20
    counter = 1
    
    for kk in range(K_START,K_END):
        K = kk
        AuxVec=1
        
        while( AuxVec <= RUN ):
            for i in range(1,RUN):
                # Generate the inputs for the iteration 
                R     = utl.makeR(NUMBER_REQUESTS)
                U,u   = utl.makeU(K)
                C     = utl.makeC(K,L)
                nAR   = utl.getRandomAR()
                D     = utl.makeD(K,nAR)
                D,o   = utl.chooseO(D)
                rho   = utl.makeRho(D,0.5)
                G     = dk.generateMultiLayerGraph(K,nAR)
                P     = utl.makeP(G)
                
                # Evalutate Each Algorithm with the above inputs 
                costPPCC[i]  = hrstc.ppcc(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
                costStatic[i]= hrstc.staticPPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
                costNaive[i] = hrstc.naive(P,D,R,rho)
                
                # Increase itter by one 
                AuxVec = AuxVec+1
                
                if (AuxVec == RUN): 
                    break
                else:
                    AuxVec = AuxVec+1
                    break
                # end For 
            #end While 

            mPPCC[counter] = np.mean(costPPCC)
            msPPCC[counter]= np.mean(costStatic) 
            mNaive[counter]= np.mean(costNaive)
            
            #printRound(kk,NUMBER_REQUESTS,rho,mPPCC(counter),mNaive(counter),msPPCC(counter),mcSimulation)
            counter = counter +1      
    # end for 






