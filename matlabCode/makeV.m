function [ V ] = makeV(R,L)
% ADDME
% Description:
%       Creates the V ( former phi ) matrix. The matrix 
%       tells us if the lth request of r, vNF type i. 
% Inputs:
%        R   :: Number of access routers for graph  
%        L   :: Graph to be returned 
%
% Return : 
%        V   :: (request)x(type_i)x(lth_function) matrix.   
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[row,col] = size(R); 
V = zeros(L,L,row); 

for i=1:row    
    for j=1:col 
        % j, iterate over the col 
        % i, in the col 
        r = R(j,i); 
        V(i,r,j) = 1;     
    end 
end 
 
end

