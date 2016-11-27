function [rute]= makeMP(G,source,nAccessRouter)
% ADDME
% Description: This makes the multiple paths and costs 
%              to each of the accesss routers from 
%              gateway tp accessrouters.  
%
%Inputs:  
%       G       :: This is the graph repping the topology
%       source  :: Source node, where the search starts from.  
%       nAR     :: The accessrouter
%       dest    :: The destination 
%            
%
% Return: 
%     mP               :: Matrix whose entries are paths 
%                           from the source to the 
%                           destination Access router. 
%     rute(pathNum,ar) :: Matrix holding the paths asso
%                           ciated to access router i. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Identify the source 

% Get the length
n = length(G); 
% Define the first destination 
dest = n-nAccessRouter+1;  

% For each access router find two paths 
for i=1:nAccessRouter
    [cost, path] = dijkstra(G,source,dest); 
    %fprintf('Path: ' repmat(), path')
    mP = fliplr(path);     
    
    for ii=1:length(mP) 
        %rute(pathNum,ii,i) = mP(ii); 
        rute(i,ii) = mP(ii); 
    end
       
    % Increment to the next access router
    dest = dest+1;   
end 
 
% Check the length of the route, if it <= 2, return null 
if(length(rute) <= 2)
    rute =0; 
end 

end 
