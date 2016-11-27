% ADDME
% Description: This is the main driver program. The
%              The program is designed to solve the
%              location and chaining and chacheing
%              problem. Using Integer linear program 
%              using: 
%                     (1) ILP() 
%                     (2) Heuristic()           
% Inputs:
%              Inputs initially defined here and feed
%              the ILP() and Heuristic() as parameters.
%              The results are returned here and used
%              to display the optimal found with ILP
%              to Heuristic(). 
%
% Terms :
%        K :: Total number of nodes
%        F :: The set containing ALL vnf's 
%        R :: Request matrix. Each row is sngl request
%             whos order is preserved
%        C :: Cost for 
%        U :: Uitlization capacity of node k
%        L :: The NUMBER of vnf  TYPES 
%        F :: The set containing all vnf's 
%        u :: CPU core requirement for vNFi
%        b :: RAM memory requirement for vNFi      
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Load the values 
% call load function 
[swCase,nAR,Sr,D,G,R,K,M,L,C,U,u] = loadData();


P   = makePaths(G); 
V   = makeV(R,L); 
rho = makeRho(D); 

% From the adjusted graph, make the new path 
% Adjust the graph, cropping the paths 
% Show the routes to the destination d  
%route_1 = makeMP(G,1,nAR); 
%adjG    = remixG(G,1,nAR,route_1); 
%route_2 = makeMP(adjG,1,nAR); 

% Plot the topology
%plotTopology(G,nAR,1,0,0);
%plotTopology(G,nAR,1,route_1,1); 
%mainplotTopology(G,nAR,1,route_2,2);

% Make the objective function and return it in a vector f 
[obj,f1,f2,f3,f4] = makeObj(K,L,R,P,V,C,D,Sr,rho); 

%----  Move this 
if ( objAssert(K,L,R,D,Sr,length(obj))~=1 )
    fprintf('Error: Objective fn len does not match its proposed length\n')
    return; 
else
    fprintf('Confirmed: Objective function variable count ..... OK\n')
end 
%----  Move this mai

%[xSol, xSolVec] = ilp(obj,f1,f2,f3,f4,K,M,L,P,R,V,C,D,Sr,U,u,rho); 



% Create the hueristic 
RUN = 30;

%[naiveVec,ppccVec,staticVec] = monteCharles(RUN,G,K,L,R,P,V,C,D,U,u,Sr,nAR,f1,f2,f3,f4,'K');         
%harryPlotter(1,naiveVec,ppccVec, staticVec,'','Number of Nodes [K]','Total Network Cost');  

%[naiveVec, ppccVec,staticVec] = monteCharles(RUN,G,K,L,R,P,V,C,D,U,u,Sr,nAR,f1,f2,f3,f4,'R');         
%harryPlotter(2,naiveVec,ppccVec,staticVec, '','Number of Requests [R]','Total Network Cost');  

%[naiveVec, ppccVec, staticVec] = monteCharles(RUN,G,K,L,R,P,V,C,D,U,u,Sr,nAR,f1,f2,f3,f4,'Rho');         
%harryPlotter(3,naiveVec,ppccVec,staticVec,'','\rho_o','Total Network Cost');  


testPrint(1,'','Number of Nodes [K]','Total Network Cost');  
testPrint(2,'','Number of Requests [R]','Total Network Cost');  
testPrint(3,'','\rho_{o}','Total Network Cost');  







