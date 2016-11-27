function [mNaive, mPPCC,msPPCC] = monteCharles(RUN,G,K,L,R,P,V,C,D,U,u,Sr,nAR,f1,f2,f3,f4,mcSimulation) 
%ADD ME 
% Description: Monte carlo driver 
 
% Inputs:  
%       
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%======================================================%
%=                   HELPER FNs                       =%
%======================================================%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : maker()
% Decr     : Create a prob. vector rho. Choose a random 
%            number bw 0 / 100 and return it in ro. 
% Input   :
%      Dk :: vector of destination nodes 
% Return   : 
%     ro  :: prob vector, indicating prob of mobility. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [ro] = maker(Dk)
        
        % asthetics
        lD = length(Dk);
        temp = zeros(1,lD);
        
        % chose D numbers
        num = 50;
        max=100;
        summ = 0;
        
        % Iterate over the entire elements in D
        for d=1:lD
            temp(d)=randi(num,1,1);
            summ = summ + temp(d);
            num = floor(num/2);
            if( d == lD )
                temp(d)= abs(summ - max);
            end
        end
        
        % Sort from smallest to largest, then flip the array
        ro = fliplr(sort(temp));
        
        if (sum(ro) > 100 )
            fprintf('Sum of probabilities exceeds max (100) ')
        end
        
        % Divide each element by 100, making the probability 0<= rho <=1
        ro = ro./100;
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : wMakeP
% Decr     : makeP wrapper function.
% Input    :
%      G  :: Graph
% Return   :
%      P  :: Shortest path cost matrix
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [P] = wMakeP(G)
        P = makePaths(G);
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : wMakeR
% Decr     : Make request wrapper function. Loop over the
%            number of requests (rows) and use randperm
%            to gen. rand nums from 1-4 of vecSize.
% Input    :
% numReq  :: Random number of requests - number of rows.
%Local Vars:
% minInt  :: min bound
%vecSize  :: The size of the vector
% numInts :: The number of ints to return
% Return   :
%     R   :: Request matrix
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [R] = wMakeR(numReq)
        vecSize = 3;
        maxInt  = 4;
        
        for rr= 1:numReq
            R(rr,:)  = randperm(maxInt,vecSize);
        end
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : wMakeV
% Decr     : Make V matrix wrapper function.
% Input    :
%
% Return   :
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [V] = wMakeV(R,L)
        V = makeV(R,L);
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : wMakeC
% Decr     : Make C matrix wrapper function.
% Input    :
%     K   :: Number of nodes
%     L   :: number of vNF
% Return   :
%     C   :: Cost Matrix
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [ C ] = wMakeC(K,L)
        C = zeros(K,L);
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : wMakeUu
% Decr     : Make V matrix wrapper function.
% Input    :
%     K   :: Number of nodes
%     L   :: number of vNF
% Return   :
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [U,u] = wMakeU(K)
        valU = [2000; 30];   
        valu1 = [40 , 10 , 20 ,30]; 
        valu2 = [ 1 , 1 , .5 , .5 ]; 
        U = repmat(valU,1,K);
        u = [valu1;valu2];  
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : wMakeD
% Decr     : Make destination vector based on number of 
%            access routers.  
% Input    :
%   nAR   :: Number of access routers
% Return   :
%     D   :: Vector containing destination nodes. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [D] = wMakeD(K,nAR)       
        D = zeros(1,nAR);
    	totalD = K+nAR; 
        count = 1; 
        for d = K+1: totalD
            D(count) = d;
            count = count + 1; 
        end
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : makeClean()
% Decr     : Clear all vars, prep for next itteration.
% Input    :
% Return   :
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function makeClean() %#ok<DEFNU>
        
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : getRandomAR()
% Decr     : Get a random number through 1-5 of AR
% Input    : NONE
% Return   :
%    num  :: Random number to return
% minInt  :: min bound
% maxInt  :: max bound
% numInts :: The number of ints to return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [num] = getRandomAR()
        minInt  = 2;
        maxInt  = 5;
        numInts = 1;
        num = randi([minInt, maxInt],[1,numInts]);
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : makeRho()
% Decr     : Create a prob. vector rho. Choose a random
%            number bw 0 / 100 and return it in ro.
% Input    :
%       Dk :: vector of destination nodes
% initialRho: The initial rho probability 
% Return   :
%      ro  :: prob vector, indicating prob of mobility.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   function [ro] = roMaker(Dk , initialRho)
        
        if(initialRho == 100 )
            ro(1) = 1;
            
            for dd=2:length(Dk)
                ro(dd)  = 0;
            end          
            
        else
            
            max = 100;
            ro(1) = initialRho / 100;
            temp(1) = 0;
            temp(2:length(Dk) -1) = sort(randperm(max - initialRho, length(Dk) -2 ));
            temp(length(Dk)) = max - initialRho;
            
            for dd=2:length(Dk)
                ro(dd)  = (temp(dd) - temp(dd - 1)) /100;
            end
            
        end
        
   end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : choose()
% Decr     : Choose a starting destination node given
%            a set of destinations.
% Input   :
%      D  :: vector of destination nodes
% Return   :
%      o  :: The graph to be returned
%      D  :: The graph to be returned
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [o,D] = chooseO(D)
        
        numm = length(D);
        rNum = randi(numm,1,1);       
        o = D(rNum);
        
        if rNum == 1
            D = [D(rNum+1:length(D))];
        else
            D = [D(1:rNum-1),D(rNum+1:length(D))] ;
        end
        
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : plotGraph()
% Decr     : Plots the randomly generated graph
% Input   :
%      G  :: The graph G to be returned
%   n_AR  :: The number of access route
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function plotGraph(G,nAR)
        plotTopology(G,nAR,1,0,0);
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : generateGraph()
% Decr     : Generates a random graph with size = K +nAR
% Input    :
%      K  :: The number of core nodes for the graph
%     nAR :: The number of Access Routers
% Locl vars:
%      n  :: The number of core nodes + num of AR
% density :: A rough estimate of the amount of edges
%  sprand :: generate adjacency matrix at random
%    tril :: Returns the elmnts below the diagonal
%   spfun :: evaluates the non-zero elements of sparse
%            matrix
% Return   :
%      A  :: The graph to be returned
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [A] = generateGraph(K,nAR)
        %n = K +40; 
         n = K+nAR;
        density = randi(2,1,1);
        A = sprand( n, n, density );
        % normalize weights to sum to num of edges
        A = tril( A, -1 );
        A = spfun( @(x) x./nnz(A), A );
        % make it symmetric (for undirected graph)
        A = A + A.';
        % Make it full again
        A = full(A);
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : trimGraph()
% Decr     : Removes jumps, moving from node to AR
% Input    :
%    nAR  :: Number of access Routers
%      A  :: The graph to be returned
% Return   :
%     cA  :: The modified/trimmed graph to be returned
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [cA] = trimGraph(A,nAR)
        [m,n] = size(A);
        cA = zeros(m,n);
        tol = 0.0001;
        roundNAR = length(A) - nAR;
        % row counter
        rCount = roundNAR + 1;
        
        % iterate over the matrix and make apt subs
        for mm=1:m
            for nn=1:n
                if( (nn > roundNAR) && (mm == 1) )
                    if( A(1,rCount) > tol || A(rCount,1) > tol)
                        cA(1,rCount) = 0.0;
                        cA(rCount,1) = 0.0;
                        rCount = rCount + 1;
                    else
                        cA(mm,nn) = A(mm,nn);
                        rCount = rCount + 1;
                    end
                else
                    cA(mm,nn) = A(mm,nn);
                end
                % Reset the counter
                if(rCount == length(A))
                    rCount = roundNAR + 1;
                end
            end
        end
        
        % Upper triangle, k=0 for everything above the upper
        cA = triu( cA, 0);
        cA = cA + cA.';
        cA = bloatGraph(cA,100);
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : trimAR()
% Decr     : Removes links between AR 
% Input    :
%    nAR  :: Number of access Routers
%      A  :: The graph to be returned
% Return   :
%     cA  :: The modified/trimmed graph to be returned
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [cA] = trimAR(cA,nAR)
        
        [m,n] = size(cA);
        start = length(cA) - nAR+1;
        
        for dd = start:m-1
            for ddd = start:m-1             
                if( cA(dd,ddd+1)~= 0 )
                    cA(dd,ddd+1) = 0;
                    cA(dd+1,ddd) = 0;
                end
            end
        end        
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : bloatGraph()
% Decr     : Multiply graph by factor
% Input   :
%  factor :: The value to be tested
%    G    :: The graph to be multiplied
% Return   :
%    rG   :: Revised graph
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function  [rG] = bloatGraph(G,val)
        rG= ceil( G.*val );
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : getVal()
% Decr     : Converts from decimal float to int.
% Input   :
%    val  :: The value to be tested
% Return   :
% retVal  :: Bool, true/false
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [retVal] = getVal(val)
        retVal = floor(val*100); 
        if (retVal <= 0 )
            retVal = 0;
        end
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : getPath()
% Decr    : Calculate the shortest path.
% Input:
%    G    :: The undirected graph
%    s    :: Source node
%    s    :: Destination node
% Rtn  :
%   cost  :: The cost of the path
%   path  :: The path elements
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [cost, path] = getPath(G,source,dest)
        % For each access router find two paths
        [cost, path] = dijkstra(G,source,dest);
        path = fliplr(path);
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : ensureLinks()
% Decr     : Verifies that there is a link from the
%            source node to the destinations nodes.
% Input   :
%      K  :: The number of nodes for the graph
%      G  :: The graph G to be returned
%   n_AR  :: The number of access routers
% Return   :
%      b  :: Bool, true/false
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [ b ] = ensureLinks_OLD(G,nAR) %#ok<DEFNU>
        b = 1;
        destStart = length(G) - nAR + 1;
        destEnd = destStart + nAR - 1;
        for ddd=destStart: destEnd
            [pCost,pPath] = getPath(G,1,ddd); 
            if (length(pPath) < 1)
                b = 0;
                fprintf('Failure: Check ensureLinks()\n')
            end
        end
        fprintf('Number of AR: %d,b: %d\n',nAR,b)
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : ensureLinks2()
% Decr     : Verifies that there is a link from the
%            source node to the destinations nodes.
% Input   :
%      K  :: The number of nodes for the graph
%      G  :: The graph G to be returned
%   n_AR  :: The number of access routers
% Return   :
%      b  :: Bool, true/false
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [ b ] = ensureLinks(G)
        debug = 0; 
        b = 1;
        [m,n] = size(G);
        for eee = 1:m
            for ddd= 1:n
                [pCost,pPath] = getPath(G,eee,ddd);
                if (pCost == Inf)
                    if(debug)
                        fprintf('----------------------------\n');
                        fprintf('Failure: Check ensureLinks()\n');
                        fprintf('pCost:%2.2f\n pPath:%d\n',pCost,pPath);
                        fprintf('----------------------------\n');
                    end
                    b = 0;
                end
            end
        end
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : monteCarloK
% Decr     : Monte carlo simulation with a varying 
%            topology size. Everything else remains 
%            constant. 
% Input   :
%      K  :: The number of nodes for the graph
%      G  :: The graph G to be returned
%     nR  :: The number of access routers
% Return   :
%  mPPCC  :: monte c ppcc avrg sol vector for each k
%  mNaive :: monte c naive avrg sol vector for each k
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [mPPCC,mNaive,msPPCC] = monteCarloK(RUN,G,R,K,L,V,P,C,D,U,u,Sr,nAR,f1,f2,f3,f4,mcSimulation) %#ok<INUSL>

        NUMBER_REQUESTS = 5;
        K_START = 10;
        K_END   = 20;
        counter = 1;
  
        for kk=K_START : K_END
            K = kk;
            AuxVec=1;
            
            while (AuxVec <= RUN )
                for i=1:RUN
                    
                    R     = wMakeR(NUMBER_REQUESTS);
                    [U,u] = wMakeU(K);
                    C     = wMakeC(K,L);
                    nAR   = getRandomAR();
                    D     = wMakeD(K,nAR);
                    [o,D] = chooseO(D);
                    rho   = maker(D);
                    G     = generateGraph(K,nAR);
                    G     = trimGraph(G,nAR);
                    G     = trimAR(G,nAR); 
                    
                    if( ensureLinks(G) == 1 )                      
                        P = wMakeP(G);
                        costPPCC(i)  = ppcc(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4);
                        costStatic(i) = staticPPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4);
                        costNaive(i) = naive(P,D,R,rho);
                        AuxVec = AuxVec+1;
                        if (AuxVec == RUN)
                            break;
                        end
                    else
                        AuxVec = AuxVec+1;
                        break;
                    end               
                end
            end
            
            mPPCC(counter)= mean(costPPCC);
            msPPCC(counter) = mean(costStatic); 
            mNaive(counter) = mean(costNaive);
            
            printRound(kk,NUMBER_REQUESTS,rho,mPPCC(counter),mNaive(counter),msPPCC(counter),mcSimulation);
            counter = counter +1;      
        end
        
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : monteCarloR
% Decr     : Monte carlo simulation with a varying 
%            request (R) size. Everything else remains 
%            constant. 
% Input   :
%      K  :: The number of nodes for the graph
%      G  :: The graph G to be returned
%     nR  :: The number of access routers
% Return   :
%  mPPCC  :: monte c ppcc avrg sol vector for each R
%  mNaive :: monte c naive avrg sol vector for each R
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [mPPCC,mNaive,msPPCC] = monteCarloR(RUN,G,R,K,L,V,P,C,D,U,u,Sr,nAR,f1,f2,f3,f4,mcSimulation) %#ok<INUSD>
        
        K     = 20;
        flag  = 0;
        [U,u] = wMakeU(K);
        C     = wMakeC(K,L);
        nAR   = 5; 
        D     = wMakeD(K,nAR);
        [o,D] = chooseO(D);
        rho   = maker(D);
        % while flag IS NOT TRUE, check that the graph is legitimate 
        while( flag ~= 1 )
            G = generateGraph(K,nAR);
            G = trimGraph(G,nAR);
            G = trimAR(G,nAR);
            if ( ensureLinks(G) == 1 )
                flag = 1;
            end
        end     
        P = wMakeP(G);
        
        R_START = 5;
        R_END   = 20;
        counter = 1;
        for rr=R_START : R_END
            AuxVec=1;
            while (AuxVec <= RUN )
                for i=1:RUN
                    R            = wMakeR(rr);
                    costPPCC(i)  = ppcc(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4);
                    costStatic(i) = staticPPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4);
                    costNaive(i) = naive(P,D,R,rho);
                    
                    AuxVec = AuxVec+1;
                end               
            end
            % Calc mean and add as single element of resp. vector. 
            mPPCC(counter)= mean(costPPCC);
            msPPCC(counter) = mean(costStatic); 
            mNaive(counter) = mean(costNaive);
            printRound(K,rr,rho,mPPCC(counter),mNaive(counter),msPPCC(counter),mcSimulation);
            counter = counter +1;          
        end
    end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : percentageDiff() 
% Decr     : Diff b/w a and b div by the avrg 
% Input    :
%     a   :: First num
%     b   :: Second num 
% Return   : 
%   diff   :: The percentage diff between a and b 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [ pDiff ] = percentageDiff(a,b) 
        pDiff = (abs(a-b)/((a+b)/2))*100;  
    end 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : monteCarloRho()
% Decr     :        
%            
% Input   :
%      K  :: The number of nodes for the graph
%      G  :: The graph G to be returned
%     nR  :: The number of access routers
% Return   :
%  mPPCC  :: monte c ppcc avrg sol vector for each R
%  mNaive :: monte c naive avrg sol vector for each R
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [mPPCC,mNaive,msPPCC] = monteCarloRho(RUN,G,R,K,L,V,P,C,D,U,u,Sr,nAR,f1,f2,f3,f4,mcSimulation)
        
        Rho_START = 0;
        Rho_END   = 100;
        NUMBER_REQUESTS = 20; 
        K     = 20;        
        flag  = 0;
        [U,u] = wMakeU(K);
        C     = wMakeC(K,L);
        R     = wMakeR(NUMBER_REQUESTS);
        nAR   = 5; 
        D     = wMakeD(K,nAR);
        [o,D] = chooseO(D);

        % while flag IS NOT TRUE, check that the graph is legitimate 
        while( flag ~= 1 )
            G = generateGraph(K,nAR);
            G = trimGraph(G,nAR);
            G = trimAR(G,nAR);
            if ( ensureLinks(G) == 1 )
                flag = 1;
            end
        end     
        
        P = wMakeP(G);
        counter = 1;      
        rr = Rho_START;
        
        while( rr <= Rho_END )
            
            AuxVec=1;
            while (AuxVec <= RUN )
                for i=1:RUN
                    rho          = roMaker(D,rr);
                    costPPCC(i)  = ppcc(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4);
                    costStatic(i)= staticPPCC(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4);
                    costNaive(i) = naive(P,D,R,rho);
                    
                    AuxVec = AuxVec+1;
                end
               
            end
            % Calc mean and add as single element of resp. vector. 
            mPPCC(counter)= mean(costPPCC);
            msPPCC(counter) = mean(costStatic); 
            mNaive(counter) = mean(costNaive);
            printRound(K,NUMBER_REQUESTS,rr,mPPCC(counter),mNaive(counter),msPPCC(counter),mcSimulation);
            counter = counter +1;          
            rr = rr + 10; 
        end
    end 


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : printRound() 
% Decr     : print the round function 
% Input    :
% numNodes :: number of nodes 
% numReq   :: Number of requests (num of rows in R) 
%     mP   :: ppcc mean solution vector of curr. round 
%     mN   :: Naive mean solution vector of curr. round 
% Return   : NONE 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function printRound(numNodes,numRequest,rhoVal,mP,mN,mS,mcSimulation)      
        fprintf('------------------------------\n');     
        fprintf('-\t\t[%s]\t\t-\n',mcSimulation);
        fprintf('------------------------------\n');     
        fprintf('Request Size   : %d\n',numRequest);
        fprintf('Topology Size  : %d\n',numNodes);
        fprintf('Rho            : %2.2f\n',rhoVal);    
        fprintf('Mean AGW       : %2.2f\n', mN);
        fprintf('Mean SPBA      : %2.2f\n', mS);
        fprintf('Mean ppcc      : %2.2f\n', mP);

    end
    


    function [avrg] = calculateAverage(data)
        
        n1 = length(data);   
        avrg = (sum(data)/n1); 
        
    end 



    function [gain] = calculateGains(data1,data2) 
        
        A = calculateAverage(data2);
        B = calculateAverage(data1);
        gain = (abs(A-B)/A)*100; 
        
    end 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : printAverageGains() 
% Decr     :
% Input    :
%   data1  :: mcMean PPCC  
%   data2  :: mcMean AGW 
%   data3  :: mcMean SPBA 
% Local Vars: 
% Return   : NONE 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function printAverageGains(data1,data2,data3,mcSimulation)
        
        
        
        fprintf('------------------------------\n');
        fprintf('-\t\tGains\t\t-\n');
        fprintf('-\t\t[%s]\t\t-\n',mcSimulation);
        fprintf('------------------------------\n');    
        fprintf('PPCC v.s. AGW : %2.2f\n',calculateGains(data1,data2) );
        fprintf('PPCC v.s. SPBA: %2.2f\n',calculateGains(data1,data3) );
        fprintf('SPBA v.s. AGW : %2.2f\n',calculateGains(data3,data2) );
        
        
    end 

%======================================================%
%=            MAIN: MONTE CARLO                       =%
%======================================================%

switch(mcSimulation)
    case 'K'
        fprintf('\nMonte Carlo simulation [K]\n')
        fprintf('----------------------------\n')
        [mPPCC,mNaive,msPPCC] = monteCarloK(RUN,G,R,K,L,V,P,C,D,U,u,Sr,nAR,f1,f2,f3,f4,mcSimulation);
        printAverageGains(mPPCC,mNaive,msPPCC,mcSimulation); 
    case 'R'
        fprintf('\nMonte Carlo simulation [R]\n')
        fprintf('----------------------------\n')
        [mPPCC,mNaive,msPPCC] = monteCarloR(RUN,G,R,K,L,V,P,C,D,U,u,Sr,nAR,f1,f2,f3,f4,mcSimulation);
        printAverageGains(mPPCC,mNaive,msPPCC,mcSimulation); 
    case 'Rho'
        fprintf('\nMonte Carlo simulation [Rho]\n')
        fprintf('----------------------------\n')
        [mPPCC,mNaive,msPPCC] = monteCarloRho(RUN,G,R,K,L,V,P,C,D,U,u,Sr,nAR,f1,f2,f3,f4,mcSimulation); 
        printAverageGains(mPPCC,mNaive,msPPCC,mcSimulation); 
    otherwise
        fprintf('Try choosing R or K for simulation type ')
end





end

