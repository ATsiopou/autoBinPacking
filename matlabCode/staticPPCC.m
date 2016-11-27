function [ cost ]  = staticPPcc(G,K,L,R,P,V,C,D,U,u,Sr,nAR,rho,o,f1,f2,f3,f4)
% ADDME
% Description: Loads data, prompt user for type ret data 
% Inputs     : 
%        K   :: The total number of nodes 
%        L   :: The number of vNFs in set F 
%        R   :: The request matrix 
%        P   :: Shortest path cost matrix 
%        V   :: 
%        C   :: The node cost matrix 
%        D   :: Desitnations vector 
%        Sr  :: Set containing starting nodes of chain  
%        nAr :: Number of access routers for graph  
%        rho :: The probability vector, given dest. 
%        U   :: Node utility constraints  
%        u   :: vNF utility requirements
% Prgm Vars   
%----------
%       CPL  :: Candidate node priority list 
%       FPL  :: Function priority list 
%    pcCost  :: allocation cost 
%        Lr  :: Length of the chain req. by r 
%         I  :: vNF chaining list
%CR_(j,j+1)  :: chaining routing costs b/w I(j)-I(j+1) 
%       CRC  :: chaining routing cost b/w I(0) to d
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%======================================================%
%=                    HELPERS                         =%
%======================================================%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : init() 
% Decr    : Initialize and declare space for algorithms 
%           variables.         
% Return  : 
% fAllocationTable:: Contains the k,l,r map combo, plus 
%                    two additional cols indicating where
%                    it failed 
% alloctionTable  :: Set size of table. Holds node,func
%                    request mapping 
%  ROW  :: K
%  COL  :: L
%  AGE  :: r
%---------------
%              R :: service request
%            r,c :: Number of rows/col of Request matrix       
%              x :: x allocation vector 
%             RU :: Remaining utility 
%              x :: x allocation vector
%             f1 :: x_k_i of objective functions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [fallocationTable,allocationTable,xTable,pcCost,RU,xfinal,r,c] = init(R,K,L,U,f1)
        [r,c] = size(R);
        xfinal = zeros(1,length(f1(:)'));
        xTable=zeros(K,L);
        RU = zeros(size(U));
        RU = U;
        allocationTable = zeros(K,L,r);
        fallocationTable = zeros(K,L,r);        
        pcCost = 0; 
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : printSummary() 
% Decr    : Prints hosting either 
%           1) successfull
%           2) failed
%           3) reason h/u
% 
% fAllocationTable:: Contains the k,l,r map combo, plus 
%                    two additional cols indicating where
%                    it failed 
% alloctionTable  :: Set size of table. Holds node,func
%                    request mapping 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function printSummary(R,K,L,D,allocationTable,fAllocationTable) 
        
        [row,col] = size(R); 
        numNodes = K; 
        
        fprintf('Desetinations:\t')
        fprintf( [ repmat('%d   ',1,size(D,2)) '\n'], D')
        %fprintf('\n')
        fprintf('Probability  : \t')
        fprintf( [ repmat('%.2f   ',1,size(rho,2)) '\n'], rho')
        fprintf('Request Matrix: \n\n')
        fprintf( [ repmat('\t%d   ',1,size(R,2)) '\n'], R')
        fprintf('\n\n')
        fprintf('-------------------------------------------------------\n');
        fprintf('Request | Order | Function  |  Mapped node | succ/fail \n');
        fprintf('-------------------------------------------------------\n');
        for rIndex=1 : row
            reqi = R(rIndex,:);
            for f=1 : L
 %               rNode = getNodeFromFunc(reqi(1,f), rIndex,numNodes,allocationTable);
 %               rFunc = reqi(f);
 %               val = fAllocationTable(rNode,rFunc,rIndex); 
 %               fprintf('   %d\t    %d\t\t%d\t   %d\t\t%d\n',rIndex,f,rFunc,rNode,val);
            end
        end
        
        
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : getDestinationNode()
% Decr    : Return the node for function f was mapped
%           to. Plot function utility.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [node] = getNodeFromFunc(func,req,K,allocationTable)
        node  = 1;
        counter = 1;
        for kInd = 1:K
            if(allocationTable(kInd,func,req) == 1)
                node = counter;
            end
            counter = counter + 1; 
        end
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : getDestinationNode() 
% Decr    : Given the destination set D, the prob. 
%           vector rho,clc. the corresponding
%           destination node. 
% Return  : 
%   node :: Node corresponding to max rho index in set D
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [node] = getDestinationNode(o)       
        % find the max val
        node = o; 
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : getStarting Node 
% Decr     : Calculate the starting node location with  
%            with the minimum cost. 
% Locl vars:
%   sNode :: The starting node  
%   minVal:: The current minimum value 
%   cost  :: Cost of the path 
%   path  :: The path, in terms of its elem. nodes. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [startingNode] = getStartNode(G,Sr,d)        
        % Choose some (relatively large) min. value to start. 
        minVal = 100;
        for ii = Sr(1):length(Sr)
            [cst,path] = getPath(G,ii,d);
            pathCost(ii) = cst;
            if ( cst <= minVal )  
                minVal = cst; 
                startingNode= path(1); 
            end 
            % Reset the cost and paths 
            path=0;
            cst=0;           
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
% Func    : getPath() 
% Decr    : wrapper function for getPath()
% Input   : 
%      s :: source
%      d :: destination 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [sNodes] = getCandidatePath(s,d)
        [cost, sNodes] = getPath(G,s,d); 
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : isHosted() 
% Decr    : Evealuates if func is hosted at node for 
%           service reqest r. 
% Input   : 
%   func :: virtual network function 
%   node :: node k
% request:: service request.
%
% Return  : 
%      b :: Bool, tf true:yes, false:no. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [b] = isHosted(node,func,request) 
        if (allocationTable(node,func,request)) 
            b = 1; 
        else 
            b = 0; 
        end 
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : host() 
% Decr    : Set the bit in the allocationTable to 1. 
%           Indicates a VNF has been placed on node for
%           request r. 
% Input   : 
%   func :: virtual network function 
%   node :: node k
% request:: service request.
%     b  :: bit, 1/0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function host(node,func,request,b)
        allocationTable(node,func,request) = b;
    end 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : setxTable()
% Decr    : Set the bit in the x vector map/table to 1. 
%           Indicates a VNF has been placed on node for
%           agnostic to request. 
% Input   : 
%   func :: virtual network function 
%   node :: node k
%    b   :: either bit to set 1/0 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function setxTable(node,func,b) 
        xTable(node,func) = b;
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : mapTicker 
% Decr    : Records the mapping, and failurs            
% Input   : 
% request:: service request.
%   func :: virtual network function 
%   node :: node k
%    b   :: either bit to set h/u
%      u :: indicates utility failure 
%      h :: indicates function isHosted at node k
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function hostFail(node,func,request,b) 
        fAllocationTable(node,func,request) = b;
    end 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : updateResources() 
% Decr    : Update the resource vector U by decreasing
%           it by u for function func. 
% Input   : 
%   func :: virtual network function 
%   node :: node k
%    U   :: Node utility 
%    u   :: function requirement 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [U] = updateResources(U,u,node,func)
        U(1,node) = U(1,node)-u(1,func);
        U(2,node) = U(2,node)-u(2,func);
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : canNodeProcess() 
% Decr    : Check to see if node has resources to process
%           the current vNF in r 
% Input   : 
%   func :: virtual network function 
%   node :: node k
%    U   :: Node utility 
%    u   :: function requirement
%
% Return  : true: yes / false:no
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [b] = canNodeProcess(U,u,node,func)       
        if( (u(1,func) <= U(1,node)) && (u(2,func) <= U(2,node) ) )
            b = 1; 
        else 
            b = 0; 
        end 
     end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func    : getNode()
% Decr    : Return the node given the function, 
%           and request
% Return  : Node 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [node] = getNode(K, func,req, allocationTable)
        node  = 1;
        counter = 1;
        for kInd = 1:K
            if(allocationTable(kInd,func,req) == 1)
                node = counter;
            end
            counter = counter + 1;
        end
    end

%======================================================%
%=                   MAIN: PPCC                       =%
%======================================================%

%- Initialization 
[fAllocationTable,allocationTable,xTable,pcCost,RU,x,r,c] = init(R,K,L,U,f1); 

d = getDestinationNode(o); 
CR = zeros(1,length(L)); 

%*  Alllocation vector  *%
for rr=1:r
    s = getStartNode(G,Sr,d);
    sNodes = getCandidatePath(s,d);
    sNodes = sNodes(1:length(sNodes) -1); %#ok<*NASGU>
    CPL = sort(s);
    FPL = R(rr,:);
    
    for kk=1:length(CPL)
        cNode=CPL(kk);
        for ff=1:length(FPL)
            cFunc = FPL(ff);
            if ( canNodeProcess(U,u,cNode,cFunc) )
                if( isHosted(cNode,cFunc,rr) == 0 )
                    host(cNode,cFunc,rr,1);
                    setxTable(cNode,cFunc,1);
                    U = updateResources(U,u,cNode,cFunc);
                    pcCost = pcCost + C(cNode,cFunc);       
                else
                    hostFail(cNode,cFunc,rr,'h');
                end
            else
                hostFail(cNode,cFunc,rr,'u');
            end
        end
    end
end


%*  Routing cost  *%
for dd=1:length(D)
    
    s = getStartNode(G,Sr,dd);
    for rr=1:r
        % length of the network elemeents
        Lr = length(R(rr,:));
        I = R(rr,:);
        for l=1:Lr-1
            n1 = getNode(K,I(l)  ,rr,allocationTable);
            n2 = getNode(K,I(l+1),rr,allocationTable);
            CR = CR + P(n1,n2);
        end
        CRC = 0;
        CRC = CRC + P(getNode(K,Lr,rr,allocationTable),D(dd));
        
        pcCost = pcCost+rho(dd)*CRC ;
    end
    
end


cost = pcCost; 

%fprintf('Cost ppcc : %2.2f\n\n', pcCost)
%printSummary(R,K,L,D,allocationTable,fAllocationTable) 

end

