import numpy as np 
import hrUtils as utl 

#======================================================#
#=                      PPCC                          =#
#======================================================#
def PPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4):
    # Print
    name="PPCC"

    #- Initialization 
    fAllocationTable,allocationTable,xTable,pcCost,RU,x,r,c = utl.init(R,K,L,U,f1)
    d = utl.getPpccDestinationNode(D,rho)
    CR = np.zeros(L)    
    
    # *Alllocation vector * #
    for rr in range (1-1, r):
        # get a single node frome the list of starting nodes
        s = utl.getStartNode(G, Sr, d)
        sNodes = utl.getCandidatePath(G, s, d)
        
        if (sNodes != 0):
            sNodes = sNodes[0:len(sNodes)-1]
            CPL = np.sort(sNodes)
            FPL = R[rr,:]

            for kk in range (0,len(CPL)):
                cNode = CPL[kk]
                for ff in range (1-1 ,len(FPL)):
                    cFunc = FPL[ff]
                    
                    if ( utl.canNodeProcess(U, u, cNode, cFunc)):
                        #if (isHosted(cNode, cFunc, rr) == 0):
                        #allocationTable = utl.host(cNode, cFunc, rr+1, 1)
                        utl.host(cNode, cFunc, rr+1, 1) ### CHANGED 
                        utl.setxTable(cNode, cFunc, 1)
                        U = utl.updateResources(U, u, cNode, cFunc)
                        pcCost = pcCost + C[cNode-1, cFunc-1]
                    else:
                        utl.hostFail(cNode, cFunc, rr+1, 404)
                    #else:
                        #hostFail(cNode, cFunc, rr, 'u')
    
    # * Routing cost * #
    for dd in range (1-1, len(D)): # reduction to to choosing o 
        s = utl.getStartNode(G, Sr, dd)
        # Define the GateWay
        GW=1
        for rr in range(1-1,r):
        # length of the network elemeents
            if ( utl.checkList(utl.blockDetector(allocationTable, R), rr+1) ):
                CRC = 0
                CRC = P[GW-1, D[dd]-1] + utl.blockingPenalty()
                pcCost = pcCost + rho[dd] * CRC
            else:
                Lr = len(R[rr,:])
                I = R[rr,:]
                for l in range (1-1,Lr-1):
                    n1 = utl.getNode(K, I[l], rr+1, allocationTable)
                    n2 = utl.getNode(K, I[l + 1], rr+1, allocationTable)
                    CR = CR + P[n1-1, n2-1]
                    CRC = 0
                    CRC = CRC + P[utl.getNode(K, Lr, rr+1, allocationTable)-1, D[dd]-1] ### SHOULD BE P[-- - 1, blah ]
                    pcCost = pcCost + rho[dd] * CRC

    cost = pcCost
                    
    # * Blocking Probability * #
    blockingProbability = float(0)
    blockedRequestlist, numberOfblockedRequest = utl.blockDetector(allocationTable, R)    
    rows,cols = R.shape
    blockingProbability = float(float(numberOfblockedRequest)/float(rows))

    #0utl.printSummary(R,K,L,D,blockingProbability,numberOfblockedRequest,blockedRequestlist ,allocationTable)   
    
    return cost, blockingProbability


# ======================================================#
# =                      BPCC                          =#
# ======================================================#
def BPCC(G, K, L, R, P, V, C, D, U, u, Sr, nAR, rho, o, f1, f2, f3, f4):
    # Define the name 
    name="BPCC"

    # - Initialization
    fAllocationTable, allocationTable, xTable, pcCost, RU, x, r, c = utl.init(R, K, L, U, f1)
    d = utl.getPpccDestinationNode(D, rho)
    CR = np.zeros(L)

    # *Alllocation vector * #
    for rr in range(1 - 1, r ):
        s = utl.getStartNode(G, Sr, d)
        sNodes = utl.getCandidatePath(G, s, d)
        if (sNodes != 0):
            sNodes = sNodes[0:len(sNodes) - 1]
            CPL = np.sort(sNodes)
            FPL = R[rr, :]

            for ff in range(1 - 1, len(FPL)):

                cFunc = FPL[ff]
                for kk in range(0, len(CPL)):
                    cNode = CPL[kk]
                    if (utl.canNodeProcess(U, u, cNode, cFunc)):
                        # if (isHosted(cNode, cFunc, rr) == 0):
                        #allocationTable = utl.host(cNode, cFunc, rr, 1)
                        utl.host(cNode, cFunc, rr+1, 1)
                        utl.setxTable(cNode, cFunc, 1)
                        U = utl.updateResources(U, u, cNode, cFunc)
                        pcCost = pcCost + C[cNode-1, cFunc-1]
                    else:
                        utl.hostFail(cNode, cFunc, rr+1, 404)
                        # else:
                        # hostFail(cNode, cFunc, rr, 'u')

    # * Routing cost * #
    for dd in range(1 - 1, len(D)):
        s = utl.getStartNode(G, Sr, dd)
        # Define the GateWay
        GW=1
        for rr in range(1 - 1, r):
            # length of the network elemeents
            if(utl.checkList(utl.blockDetector(allocationTable, R), rr+1)):
                CRC = 0
                CRC = P[GW - 1 , D[dd] - 1] + utl.blockingPenalty()
                pcCost = pcCost + rho[dd]*CRC
            else:
                Lr = len(R[rr, :])
                I = R[rr, :]
                for l in range(1 - 1, Lr-1):
                    n1 = utl.getNode(K, I[l], rr+1, allocationTable)
                    n2 = utl.getNode(K, I[l + 1], rr+1, allocationTable)
                    CR = CR + P[n1-1, n2-1]
                    CRC = 0
                    CRC = CRC + P[utl.getNode(K, Lr, rr+1, allocationTable)-1, D[dd] - 1]
                    pcCost = pcCost + rho[dd] * CRC
    cost = pcCost

    # * Blocking Probability * #
    blockingProbability = float(0)
    blockedRequestlist, numberOfblockedRequest = utl.blockDetector(allocationTable, R)
    rows, cols = R.shape
    blockingProbability = float(float(numberOfblockedRequest) / float(rows)) 
    
    #utl.printSummary(R,K,L,D,blockingProbability,numberOfblockedRequest,blockedRequestlist ,allocationTable)    

    return cost, blockingProbability


#======================================================#
#=        SPBA  : Shortest Path Based Allocation      =#
#======================================================#
def SPBA(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4):

    name="SPBA"
    #- Initialization
    fAllocationTable,allocationTable,xTable,pcCost,RU,x,r,c = utl.init(R,K,L,U,f1)
    d = utl.getStaticDestinationNode(o)
    CR = np.zeros(L)
   
    # *Alllocation vector * #
    for rr in range (1-1, r):
        s = utl.getStartNode(G, Sr, d)
        sNodes = utl.getCandidatePath(G, s, d)

        if (sNodes != 0):
            sNodes = sNodes[0:len(sNodes) - 1]
            CPL = np.sort(sNodes)
            FPL = R[rr,:]

            for kk in range (1,len(CPL)):
                cNode = CPL[kk]
                for ff in range (1-1 ,len(FPL)):
                    cFunc = FPL[ff]
                    if (utl.canNodeProcess(U, u, cNode, cFunc)):
                        #allocationTable = utl.host(cNode, cFunc, rr, 1)
                        utl.host(cNode, cFunc, rr+1, 1)
                        utl.setxTable(cNode, cFunc, 1)
                        U = utl.updateResources(U, u, cNode, cFunc)
                        pcCost = pcCost + C[cNode-1, cFunc-1]
                    else:
                        utl.hostFail(cNode, cFunc, rr+1, 404)
                    #else:
                    #hostFail(cNode, cFunc, rr, 'u')

    # * Routing cost * #
    for dd in range (1-1, len(D)):

        s = utl.getStartNode(G, Sr, dd)
        # Define the GateWay
        GW=1
        for rr in range(1-1,r):
        # length of the network elemeents
            if ( utl.checkList(utl.blockDetector(allocationTable, R), rr+1) ):
                CRC = 0
                CRC = P[GW-1, D[dd]-1]+utl.blockingPenalty()
                pcCost = pcCost + rho[dd]*CRC
            else:
                Lr = len(R[rr,:])
                I = R[rr,:]
                for l in range (1-1,Lr-1):
                    n1 = utl.getNode(K, I[l], rr+1, allocationTable)
                    n2 = utl.getNode(K, I[l + 1], rr+1, allocationTable)
                    CR = CR + P[n1-1, n2-1]
                    CRC = 0
                    CRC = CRC + P[utl.getNode(K, Lr, rr+1, allocationTable)-1, D[dd] - 1]
                    pcCost = pcCost + rho[dd] * CRC
    cost = pcCost

    # * Blocking Probability * #
    blockingProbability = float(0)
    blockedRequestlist, numberOfblockedRequest = utl.blockDetector(allocationTable, R)
    rows,cols = R.shape
    blockingProbability = float(float(numberOfblockedRequest)/float(rows))

    # Testing printout - to confirm blocking probability works correctly 
    #utl.printSummary(R,K,L,D,blockingProbability,numberOfblockedRequest,blockedRequestlist ,allocationTable)    

    return cost , blockingProbability
#======================================================#
#=            AGW   :   All from GateWay              =#
#======================================================#
def AGW(P,D,R,rho):
    name="AGW"
    
    # Define the GateWay
    GW = 1
    sumCost = 0
    rrr, c = R.shape

    for rr in range (1-1, rrr):
        for dd in range (1-1, len(D)):
            sumCost = sumCost + rho[dd] * P[GW-1, D[dd]-1]
    cost = sumCost
    return cost
#======================================================#
#=      CAGW   : Capacitated All from GateWay         =#
#======================================================#
def CAGW(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4):

    name="CAGW"
    
    # Define the GateWay
    GW = 1
    # - Initialization
    fAllocationTable, allocationTable, xTable, pcCost, RU, x, r, c = utl.init(R, K, L, U, f1)

    for rr in range (1-1, r):
        FPL = R[rr,:]
        cNode = GW 
        for ff in range (1-1 ,len(FPL)):
            cFunc = FPL[ff] - 1
            if (utl.canNodeProcess(U, u, cNode, cFunc)):
                #if (isHosted(cNode, cFunc, rr) == 0):
                #allocationTable = utl.host(cNode, cFunc, rr, 1)
                utl.host(cNode, cFunc, rr+1, 1)
                utl.setxTable(cNode, cFunc, 1)
                U = utl.updateResources(U, u, cNode, cFunc)
                pcCost = pcCost + C[cNode-1, cFunc-1]
            else:
                utl.hostFail(cNode, cFunc, rr+1, 404)

    # * Routing cost * #
    rrr, c = R.shape

    for dd in range(1 - 1, len(D)):
        for rr in range (1-1, rrr):
            if (utl.checkList(utl.blockDetector(allocationTable, R), rr+1)):
                CRC = 0
                CRC = P[GW-1, D[dd]-1] + utl.blockingPenalty()
                pcCost = pcCost + rho[dd] * CRC
            else:
                CRC = 0
                CRC = P[GW-1, D[dd]-1]
                pcCost = pcCost + rho[dd] * CRC

    cost = pcCost

    # * Blocking Probability * #
    blockingProbability = float(0)
    blockedRequestlist, numberOfblockedRequest = utl.blockDetector(allocationTable, R)
    rows, cols = R.shape
    blockingProbability = float( float(numberOfblockedRequest) / float(rows) ) 
    
    #utl.printSummary(R,K,L,D,blockingProbability,numberOfblockedRequest,blockedRequestlist ,allocationTable)    
    
    return cost, blockingProbability



    
