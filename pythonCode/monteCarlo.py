import hrUtils as utl 
import heuristic as hrstc 
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
def monteCarlo(simType,RUN,Sr,L,V,f1,f2,f3,f4):
    
    if ( simType == 'K' ):
    # This simulates monte carlo for nodes K
        mPPCC,mSPBA,mBPCC,mAGW,mCAGW, mbPPCC, mbSPBA, mbBPCC, mbCAGW = monteCarloK(RUN,Sr,L,V,f1,f2,f3,f4,simType)
        #printAverageGains(mPPCC,mSPBA,mAGW,simType)
        print "mPPCC :", mPPCC
        print "mSPBA :", mSPBA
        print "mBPCC :", mBPCC
        print "mAGW :", mAGW
        print "mCAGW :", mCAGW
        print "mbPPCC :", mbPPCC
        print "mbSPBA :", mbSPBA
        print "mbBPCC :", mbBPCC
        print "mbCAGW :", mbCAGW
    elif ( simType == 'R' ):
    # Simulate monte carlo for Requeasts
        print "-"*20
        print "Monte Carlo simulation [R]" 
        print "-"*20
        mPPCC,mSPBA,mBPCC,mAGW,mCAGW = monteCarloR(RUN,Sr,L,V,f1,f2,f3,f4,simType)        
        printAverageGains(mPPCC,mSPBA,mAGW,simType) 

    elif( simType == 'Rho' ):
    # Simulate Rho change in monte Carlo
        print "-"*20
        print"Monte Carlo simulation [Rho]"
        print "-"*20
        mPPCC,mSPBA,mBPCC,mAGW,mCAGW = monteCarloRho(RUN,Sr,L,V,f1,f2,f3,f4,simType)
        printAverageGains(mPPCC,mSPBA,mAGW,simType) 
    
    else:
        return 0

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
def monteCarloK(RUN,Sr,L,V,f1,f2,f3,f4,simType): 

    print "RUN IN MONTECARLOK: " , RUN 

    # Init the vectors of size 1xRUN 
    costPPCC = np.zeros((RUN), dtype=np.int)
    costSPBA = np.zeros((RUN), dtype=np.int) 
    costBPCC = np.zeros((RUN), dtype=np.int) 
    costAGW  = np.zeros((RUN), dtype=np.int)
    costCAGW = np.zeros((RUN), dtype=np.int)
    blockPPCC = np.zeros((RUN), dtype=np.float)
    blockSPBA = np.zeros((RUN), dtype=np.float)
    blockBPCC = np.zeros((RUN), dtype=np.float)
    blockCAGW = np.zeros((RUN), dtype=np.float)

    # Init the mean vectors 
    mPPCC = np.zeros((RUN), dtype=np.int) 
    mSPBA = np.zeros((RUN), dtype=np.int)
    mBPCC = np.zeros((RUN), dtype=np.int)
    mAGW  = np.zeros((RUN), dtype=np.int)
    mCAGW = np.zeros((RUN), dtype=np.int)
    mbPPCC = np.zeros((RUN), dtype=np.float)
    mbSPBA = np.zeros((RUN), dtype=np.float)
    mbBPCC = np.zeros((RUN), dtype=np.float)
    mbCAGW = np.zeros((RUN), dtype=np.float)

    # Init the monte carlo vars 
    NUMBER_REQUESTS = 5
    NUMBER_VNFS = 5
    LENGTH_REQUESTS = 3
    K_START = 10
    K_END   = 20
    counter = 0

    # Start the main iteration loop 
    for kk in range(K_START,K_END):
        K = kk
        #AuxVec = 1
        #while( AuxVec <= RUN ):
        for i in range(0,RUN):
            # Generate the inputs for the iteration
            R     = utl.makeR(NUMBER_REQUESTS,NUMBER_VNFS, LENGTH_REQUESTS)
            U,u   = utl.makeU(K)
            C     = utl.makeC(K,L)
            nAR   = utl.getRandomAR()
            D     = utl.makeD(K,nAR)
            D,o   = utl.chooseO(D)
            rho   = utl.makeRho(D,1)
            G     = dk.generateMultiLayerGraph(K,nAR)
            P     = utl.makeP(G)
                
            print "Iteration : " , i

            # Evalutate Each Algorithm with the above inputs
            cost1,block1 = hrstc.PPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
            cost2,block2 = hrstc.SPBA(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
            cost3,block3 = hrstc.BPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
            cost4,block4 = hrstc.CAGW(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
            cost5 = hrstc.AGW(P,D,R,rho)
            
            if(cost1 == 0 or cost2 == 0 or cost3 == 0 or cost4 == 0 or cost5 == 0 ):
                i = i-1
            else :
                costPPCC[i] = cost1
                costSPBA[i] = cost2
                costBPCC[i] = cost3
                costCAGW[i] = cost4
                costAGW[i]  = cost5
           
                blockPPCC[i] = block1
                blockSPBA[i] = block2
                blockBPCC[i] = block3
                blockCAGW[i] = block4
            #AuxVec = AuxVec + 1;

        print "costPPCC : " , costPPCC
        print "costSPBA : " , costSPBA
        print "costBPCC : " , costBPCC
        print "costCAGW : ", costCAGW 
        print "costAGW  : ", costAGW 
        
        print "blockPPCC :" , blockPPCC
        print "blockSPBA :" , blockSPBA
        print "blockBPCC :" , blockBPCC
        print "blockCAGW :" , blockCAGW
        
        mPPCC[counter]= np.mean(costPPCC)
        mSPBA[counter]= np.mean(costSPBA)
        mBPCC[counter]= np.mean(costBPCC)
        mCAGW[counter] = np.mean(costCAGW)
        mAGW[counter] = np.mean(costAGW)
        mbPPCC[counter] = np.mean(blockPPCC)
        mbSPBA[counter] = np.mean(blockSPBA)
        mbBPCC[counter] = np.mean(blockBPCC)
        mbCAGW[counter] = np.mean(blockCAGW)
        
        printRound(kk,NUMBER_REQUESTS,rho,mPPCC[counter],mSPBA[counter],mBPCC[counter],mCAGW[counter],mAGW[counter],mbPPCC[counter],mbSPBA[counter],mbBPCC[counter],mbCAGW[counter])
        counter = counter +1      
    # end for 
    return mPPCC,mSPBA,mBPCC,mAGW,mCAGW, mbPPCC, mbSPBA, mbBPCC, mbCAGW



###########################################################    
# Func     : monteCarloR
# Decr     : Monte carlo simulation with a varying 
#            request (R) size. Everything else remains 
#            constant. 
# Input   :
#      K  :: The number of nodes for the graph
#      G  :: The graph G to be returned
#     nR  :: The number of access routers
# Return   :
#  mPPCC  :: monte c ppcc avrg sol vector for each R
#  mNaive :: monte c naive avrg sol vector for each R
###########################################################    
def monteCarloR(RUN,Sr,L,V,f1,f2,f3,f4,simType): 
        
    # Init the vectors of size 1xRUN 
    costPPCC = np.zeros((RUN), dtype=np.int)
    costSPBA = np.zeros((RUN), dtype=np.int) 
    costBPCC = np.zeros((RUN), dtype=np.int) 
    costAGW  = np.zeros((RUN), dtype=np.int)
    costCAGW = np.zeros((RUN), dtype=np.int)

    # Init the mean vectors 
    mPPCC = np.zeros((RUN), dtype=np.int) 
    mSPBA = np.zeros((RUN), dtype=np.int)
    mBPCC = np.zeros((RUN), dtype=np.int)
    mAGW  = np.zeros((RUN), dtype=np.int)
    mCAGW = np.zeros((RUN), dtype=np.int)

    # Define/init local vars 
    K     = 20
    nAR   = 5 
    flag  = 0
    U,u   = utl.makeU(K)
    C     = utl.makeC(K,L)
    D     = utl.makeD(K,nAR)
    D,o   = utl.chooseO(D)
    rho   = utl.makeRho(D,100)
    # while flag IS NOT TRUE, check that the graph is legitimate 
    G     = dk.generateMultiLayerGraph(K,nAR)    
    P     = utl.makeP(G)
    NUMBER_VNFS = 5
    LENGTH_REQUESTS = 3

    # Vars for the loop 
    R_START = 5;
    R_END   = 20;
    counter = 1;
    
    for rr in range(R_START,R_END):
        AuxVec=1;
        while (AuxVec <= RUN ):
            for i in range(0,RUN): 
                R     = utl.makeR(rr,NUMBER_VNFS,LENGTH_REQUESTS)
                # Evalutate Each Algorithm with the above inputs 
                cost1,block1 = hrstc.PPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
                cost2,block2 = hrstc.SPBA(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
                cost3,block3 = hrstc.BPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
                cost4,block4 = hrstc.CAGW(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
                cost5 = hrstc.AGW(P,D,R,rho)
                AuxVec = AuxVec+1;
                
        # Calc mean and add as single element of resp. vector. 
        mPPCC[counter]= np.mean(costPPCC)
        mSPBA[counter]= np.mean(costSPBA)
        mBPCC[counter]= np.mean(costBPCC)
        mCAGW[counter] = np.mean(costCAGW)
        mAGW[counter] = np.mean(costAGW)
    
        #printRound(K,rr,rho,mPPCC(counter),mNaive(counter),msPPCC(counter),mcSimulation);
        counter = counter +1;          
    return mPPCC,mSPBA,mBPCC,mAGW,mCAGW


###########################################################
# Func     : monteCarloRho()
# Decr     :        
#           
# Input   :
#      K  :: The number of nodes for the graph
#      G  :: The graph G to be returned
#     nR  :: The number of access routers
# Return   :
#  mPPCC  :: monte c ppcc avrg sol vector for each R
#  mNaive :: monte c naive avrg sol vector for each R
###########################################################    
def monteCarloRho(RUN,Sr,L,V,f1,f2,f3,f4,simType):         
    # Init the vectors of size 1xRUN 
    costPPCC = np.zeros((RUN), dtype=np.int)
    costSPBA = np.zeros((RUN), dtype=np.int) 
    costBPCC = np.zeros((RUN), dtype=np.int) 
    costAGW  = np.zeros((RUN), dtype=np.int)
    costCAGW = np.zeros((RUN), dtype=np.int)

    # Init the mean vectors 
    mPPCC = np.zeros((RUN), dtype=np.int) 
    mSPBA = np.zeros((RUN), dtype=np.int)
    mBPCC = np.zeros((RUN), dtype=np.int)
    mAGW  = np.zeros((RUN), dtype=np.int)
    mCAGW = np.zeros((RUN), dtype=np.int)

    # Define/init local vars 
    K     = 20
    flag  = 0
    Dk = 0 
    Rho_START = 0
    Rho_END   = 100
    NUMBER_REQUESTS = 20
    NUMBER_VNFS = 5
    LENGTH_REQUESTS = 3

    # while flag IS NOT TRUE, check that the graph is legitimate 
    nAR   = 5 
    U,u   = utl.makeU(K)
    C     = utl.makeC(K,L)
    R     = utl.makeR(NUMBER_REQUESTS,NUMBER_VNFS,LENGTH_REQUESTS)
    D     = utl.makeD(K,nAR)
    D,o   = utl.chooseO(D)
    G     = dk.generateMultiLayerGraph(K,nAR)    
    P     = utl.makeP(G)

    counter = 1     
    rr = Rho_START
        
    while( rr <= Rho_END ):
        #AuxVec = 1 
        #while (AuxVec <= RUN ):
        for i in range(1,RUN):
            rho   = utl.makeRho(D,1)
            # Evalutate Each Algorithm with the above inputs 
            cost1,block1 = hrstc.PPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
            cost2,block2 = hrstc.SPBA(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
            cost3,block3 = hrstc.BPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
            cost4,block4 = hrstc.CAGW(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
            cost5 = hrstc.AGW(P,D,R,rho)
            #AuxVec = AuxVec+1;
            
            # Calc mean and add as single element of resp. vector. 
        mPPCC[counter]= np.mean(costPPCC)
        mSPBA[counter]= np.mean(costSPBA)
        mBPCC[counter]= np.mean(costBPCC)
        mCAGW[counter] = np.mean(costCAGW)
        mAGW[counter] = np.mean(costAGW)
        #printRound(K,NUMBER_REQUESTS,rr,mPPCC(counter),mNaive(counter),msPPCC(counter),mcSimulation);
        counter = counter +1;          
        
        rr = rr + 10; 
        # End 1 while 
    return mPPCC,mSPBA,mBPCC,mAGW,mCAGW
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
    print " PPCC v.s. AGW : " , calculateGains(d1,d2)
    print " PPCC v.s. SPBA: " , calculateGains(d1,d3)
    print " SPBA v.s. AGW : " , calculateGains(d3,d2)
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
    gain = float(float((float(abs(float(a)-float(b)))/float(a)))*100.00)
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
    avrg = float((float(sum(d))/float(n1)))
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
def printRound(kk,NUMBER_REQUESTS,rho,mPPCC,mSPBA,mBPCC,mCAGW,mAGW,mbPPCC,mbSPBA,mbBPCC,mbCAGW):
    print "-"*15
    #print "-\t\t[" ,mcSimulation ,"]\t\t-"
    print "-"*15 
    print "Topology Size\t:"  , kk
    print "Request Size\t:" , NUMBER_REQUESTS
    print "Rho\t\t:"         , rho
    print "Mean PPCC\t:"      , mPPCC
    print "Mean SPBA\t:"     , mSPBA
    print "Mean BPCC\t:"     , mBPCC
    print "Mean CGAW\t:", mCAGW
    print "Mean AGW\t:", mAGW
    print "Mean Blocking PPCC\t:", mbPPCC
    print "Mean Blocking SPBA\t:", mbSPBA
    print "Mean Blocking BPCC\t:", mbBPCC
    print "Mean Blocking CAGW\t:", mbCAGW
