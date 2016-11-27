function [ cost ] = naive(P,D,R,rho)
%ADD ME 
% Description: Creates the 6th set of constraints 
%
% Inputs:  
%        K :: Total number of nodes 
%        M :: Total number of nodes 
%        L :: The total number of functions 
%        R :: Request matrix. Each row is sngl request 
%           
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


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



%======================================================%
%=                   MAIN: Naive                      =%
%======================================================%


% Define the gateway 
GW = 1;

% Get the first destination 
%d1 = getDestinaion(D,rho)
%pathCost1 = P(GW,d1); 

sumCost = 0; 
[rrr, c ] = size(R); 

for rr = 1:rrr 
    for dd = 1 : length(D)    
    
        sumCost = sumCost + rho(dd) * P(GW,D(dd)); 

    end 
end     
cost = sumCost; 

end

