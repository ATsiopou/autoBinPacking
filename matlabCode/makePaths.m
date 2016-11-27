function [P] = makePaths(G)
% ADDME
% Description: 
%           Fucntion to calculate the shortest 
%           path k to m 
% Inputs:      
%       
%         
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Add a condition for no via node
n = length(G);
for kk=1:n 
    for mm=1:n 
        if kk==mm
            P(kk,mm) = 0; 
        end       
        [cost,path] = dijkstra(G,kk,mm);
        P(kk,mm) = cost; 
    end
end 
end 


