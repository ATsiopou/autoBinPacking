import numpy as np 
import hrUtils as utl 

#======================================================#
#=                      PPCC                          =#
#======================================================#
def PPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4):

#- Initialization 
    fAllocationTable,allocationTable,xTable,pcCost,RU,x,r,c = utl.init(R,K,L,U,f1)

    d = utl.getPpccDestinationNode(D,rho)
    CR = np.zeros((1,L))
    
    
    # *Alllocation vector * #
    for rr in range (1-1, r-1):
        s = utl.getStartNode(G, Sr, d)
        sNodes = utl.getCandidatePath(s, d)
        sNodes = sNodes[1:len(sNodes)-1]
        CPL = np.sort(s)
        FPL = R[rr,:]

        for kk in range (1,len(CPL)):
            cNode = CPL[kk]
            for ff in range (1-1 ,len(FPL)-1):
                cFunc = FPL[ff]
                if ( utl.canNodeProcess(U, u, cNode, cFunc)):
                    #if (isHosted(cNode, cFunc, rr) == 0):
                    utl.host(cNode, cFunc, rr, 1)
                    utl.setxTable(cNode, cFunc, 1)
                    U = utl.updateResources(U, u, cNode, cFunc)
                    pcCost = pcCost + C[cNode, cFunc]
                else:
                    utl.hostFail(cNode, cFunc, rr, 'h')
                #else:
                    #hostFail(cNode, cFunc, rr, 'u')
    
    # * Routing cost * #
    for dd in range (1-1, len(D)-1):

        s = utl.getStartNode(G, Sr, dd)
        GW=1
        for rr in range(1-1,r-1):
        # length of the network elemeents
            if (rr in utl.blockDetector(allocationTable, R)):
                CRC = 0
                CRC = P[GW, D[dd]] + utl.blockingPenalty

                pcCost = pcCost + rho(dd) * CRC
            else:
                Lr = len(R[rr,:])
                I = R[rr,:]
                for l in range (1-1,(Lr - 1)-1):
                    n1 = utl.getNode(K, I(l), rr, allocationTable)
                    n2 = utl.getNode(K, I(l + 1), rr, allocationTable)
                    CR = CR + P[n1, n2]
                    CRC = 0
                    CRC = CRC + P(utl.getNode(K, Lr, rr, allocationTable), D[dd])

                    pcCost = pcCost + rho[dd] * CRC

    cost = pcCost

# * Blocking Probability * #
    blockingProbability = float(0)
    blockedRequestlist, numberOfblockedRequest = utl.blockDetector (allocationTable, R)
    rows,cols = R.shape
    blockingProbability = float(numberOfblockedRequest)/float(rows)

        #print('Cost ppcc : #2.2f\n\n', pcCost)
        #printSummary(R,K,L,D,allocationTable,fAllocationTable)
    return cost, blockingProbability


# ======================================================#
# =                      BPCC                          =#
# ======================================================#
def BPCC(G, K, L, R, P, V, C, D, U, u, Sr, nAR, rho, o, f1, f2, f3, f4):
    # - Initialization
    fAllocationTable, allocationTable, xTable, pcCost, RU, x, r, c = utl.init(R, K, L, U, f1)

    d = utl.getPpccDestinationNode(D, rho)
    CR = np.zeros((1, L))

    # *Alllocation vector * #
    for rr in range(1 - 1, r - 1):
        s = utl.getStartNode(G, Sr, d)
        sNodes = utl.getCandidatePath(s, d)
        sNodes = sNodes[1:len(sNodes) - 1]
        CPL = np.sort(s)
        FPL = R[rr, :]

        for ff in range(1 - 1, len(FPL) - 1):
            cNode = CPL[ff]
            for kk in range(1, len(CPL)):
                cFunc = FPL[kk]
                if (utl.canNodeProcess(U, u, cNode, cFunc)):
                    # if (isHosted(cNode, cFunc, rr) == 0):
                    utl.host(cNode, cFunc, rr, 1)
                    utl.setxTable(cNode, cFunc, 1)
                    U = utl.updateResources(U, u, cNode, cFunc)
                    pcCost = pcCost + C[cNode, cFunc]
                else:
                    utl.hostFail(cNode, cFunc, rr, 'h')
                    # else:
                    # hostFail(cNode, cFunc, rr, 'u')

    # * Routing cost * #
    for dd in range(1 - 1, len(D) - 1):

        s = utl.getStartNode(G, Sr, dd)
        GW=1
        for rr in range(1 - 1, r - 1):
            # length of the network elemeents
            if(rr in utl.blockDetector(allocationTable,R)):
                CRC = 0
                CRC = P[GW, D[dd]]+utl.blockingPenalty

                pcCost = pcCost + rho(dd)*CRC
            else:
                Lr = len(R[rr, :])
                I = R[rr, :]
                for l in range(1 - 1, (Lr - 1) - 1):
                    n1 = utl.getNode(K, I(l), rr, allocationTable)
                    n2 = utl.getNode(K, I(l + 1), rr, allocationTable)
                    CR = CR + P[n1, n2]
                    CRC = 0
                    CRC = CRC + P(utl.getNode(K, Lr, rr, allocationTable), D[dd])

                    pcCost = pcCost + rho[dd] * CRC

    cost = pcCost

    # * Blocking Probability * #
    blockingProbability = float(0)
    blockedRequestlist, numberOfblockedRequest = utl.blockDetector(allocationTable, R)
    rows, cols = R.shape
    blockingProbability = float(numberOfblockedRequest) / float(rows)

        # print('Cost ppcc : #2.2f\n\n', pcCost)
        # printSummary(R,K,L,D,allocationTable,fAllocationTable)
    return cost, blockingProbability


#======================================================#
#=        SPBA  : Shortest Path Based Allocation      =#
#======================================================#
def SPBA(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4):

#- Initialization
    fAllocationTable,allocationTable,xTable,pcCost,RU,x,r,c = utl.init(R,K,L,U,f1)

    d = utl.getStaticDestinationNode(o)
    CR = np.zeros((1,len(L)))
    # *Alllocation vector * #
    for rr in range (1-1, r-1):
        s = utl.getStartNode(G, Sr, d)
        sNodes = utl.getCandidatePath(s, d)
        sNodes = sNodes[1:len(sNodes) - 1]#  # ok<*NASGU>
        CPL = np.sort(s)
        FPL = R[rr,:]

        for kk in range (1,len(CPL)):
            cNode = CPL[kk]
            for ff in range (1-1 ,len(FPL)-1):
                cFunc = FPL[ff]
                if (utl.canNodeProcess(U, u, cNode, cFunc)):
                    #if (isHosted(cNode, cFunc, rr) == 0):
                    utl.host(cNode, cFunc, rr, 1)
                    utl.setxTable(cNode, cFunc, 1)
                    U = utl.updateResources(U, u, cNode, cFunc)
                    pcCost = pcCost + C(cNode, cFunc)
                else:
                    utl.hostFail(cNode, cFunc, rr, 'h')
                #else:
                    #hostFail(cNode, cFunc, rr, 'u')

    # * Routing cost * #
    for dd in range (1-1, len(D)-1):

        s = utl.getStartNode(G, Sr, dd)
        GW=1
        for rr in range(1-1,r-1):
        # length of the network elemeents
            if(rr in utl.blockDetector(allocationTable,R)):
                CRC = 0
                CRC = P[GW, D[dd]]+utl.blockingPenalty

                pcCost = pcCost + rho(dd)*CRC
            else:
                Lr = len(R[rr,:])
                I = R[rr,:]
                for l in range (1-1,(Lr - 1)-1):
                    n1 = utl.getNode(K, I(l), rr, allocationTable)
                    n2 = utl.getNode(K, I(l + 1), rr, allocationTable)
                    CR = CR + P(n1, n2)
                    CRC = 0
                    CRC = CRC + P(utl.getNode(K, Lr, rr, allocationTable), D[dd])

                    pcCost = pcCost + rho(dd) * CRC

    cost = pcCost

    # * Blocking Probability * #
    blockingProbability = float(0)
    blockedRequestlist, numberOfblockedRequest = utl.blockDetector (allocationTable, R)
    rows,cols = R.shape
    blockingProbability = float(numberOfblockedRequest)/float(rows)




        #print('Cost ppcc : #2.2f\n\n', pcCost)
        #printSummary(R,K,L,D,allocationTable,fAllocationTable)
    return cost , blockingProbability

#======================================================#
#=            AGW   :   All from GateWay              =#
#======================================================#
def AGW(P,D,R,rho):
    # Define the GateWay
    GW = 1

    # Get the first destination
    # d1 = getDestinaion(D, rho)
    # pathCost1 = P(GW, d1);

    sumCost = 0
    rrr, c = R.shape

    for rr in range (1-1, rrr-1):
        for dd in range (1-1, len(D)-1):

            sumCost = sumCost + rho[dd] * P[GW, D[dd]]

    cost = sumCost

    return cost