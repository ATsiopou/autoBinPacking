function [Aeq,beq] = makeABeq(R,K,M,L,matwid)
%ADD ME 
% Description: Creates 8 total constraints 
%
% Inputs:  
%        K :: Total number of nodes 
%        M :: Total number of nodes 
%        L :: The total number of functions 
%        R :: Request matrix. Each row is sngl request 
%             whos order is preserved
%   matwid :: Matrix width, length of objective func.     
% 
% Notes:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Call associated function to their constraints 
[C_9,bi9] = C9(R,K,M,L,matwid); 

% Get the size 
[row9,col9] = size(C_9);  

%make the filler 
filler9 = zeros(row9,matwid - col9); 

% Cnstruct the Equality matrix and the equality vector b 
Aeq = [C_9 filler9]; 
beq = [bi9]; 


end 


