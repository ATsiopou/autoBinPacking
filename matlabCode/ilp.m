function [ xSol, xSolVec ] = ilp(obj,f1,f2,f3,f4,K,M,L,P,R,V,C,D,Sr,U,u,rho)
% ADDME
% Description: Solves the ILP problem for routing and 
%              chaining and proactive placement of vNF. 
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
%    matwid  :: The width of A, given from OBJ fn length 
%
% Return     :
%
%       xSol :: Solution from the ILP 
%    xSolVec :: The binary solution vector  
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Get the number of requests 
[r,cols] = size(R); 
matwid = length(obj); 

% Create A inequality and binequality 
%[Aineq,bineq] = makeABin(R,K,M,L,B,U,b,u,matwid); 

% Create Aequality and bequality 
[Aeq,beq] = makeABeq(R,K,M,L,matwid); 

options = optimoptions('intlinprog','Display','iter','MaxTime',7200);
% Lower/Upper/intcon defined here
intcon = 1:matwid;
% Upper and Lower bounds 
lb = zeros(matwid,1);
ub = ones(matwid,1);

%ilp_sol is the optimal
[xSol,xSolVec] = intlinprog(obj,intcon,Aineq,bineq,Aeq,beq,lb,ub,options); 





end

