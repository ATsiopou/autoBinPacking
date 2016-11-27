function [newG] = remixG(G,nGateway,nAccessRouter,rute)
% ADDME
% Description: This function remakes the topology G 
%              to a newG (topology) discounting the 
%              optimal routes. This function is to be 
%              used in conj. with makeMP to construct 
%              optimal/sub-opt routes. 
%Inputs:      
%  G            :: Topology 
%  nGateway     :: Number of gateways 
%  nAccessRouter:: Number of access routers(endNodes) 
%   rute        :: The optimal rute, sub rute. These 
%                   are the links to be removed 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


n = length(G); 


[row,col] = size(rute); 
% Make a copy of G 
newG = G; 

% Initialize jj 
jj = 0; 
% Draw the routes for each path
for rr=1:row
    % Assign a row of matrix of paths to variable r
    r = rute(rr,:); 
    % Assign a different color to each flow
    for ii=1:col  
        jj = ii+1;  
        %fprintf('%d -- %d \t\t G: %d \t nG: %d \n', r(ii), r(jj),G(r(ii),r(jj)),newG(r(ii),r(jj)))
        %now set the value of newG = to 0 
        if(r(ii) == 0 || r(jj) == 0 )
            break; 
        else 
            newG(r(ii),r(jj)) = 0;
            newG(r(jj),r(ii)) = 0; 
        end 
            %fprintf('%d -- %d \t\t G: %d \t nG: %d \n', r(ii), r(jj),G(r(ii),r(jj)),newG(r(ii),r(jj)))
        if(jj>=col) 
            break; 
        end
    end
end 




end 