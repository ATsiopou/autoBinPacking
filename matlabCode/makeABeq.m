function [Aineq,bineq]=makeABin(R,K,M,L,B,U,b,u,matwid)
%ADD ME 
% Description: Creates the 6th set of constraints 
%
% Inputs:  
%        K :: Total number of nodes 
%        M :: Total number of nodes 
%        L :: The total number of functions 
%        R :: Request matrix. Each row is sngl request 
%             whos order is preserved
%   matwid :: Matrix width, length of objective func.     
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% CONSTRAINT 1 and 2
[C_12,bi12] = C12(R,K,L,B,U,b,u,matwid); 











































% CONSTRAINT 3
%[C_3,bi3] = C3(R,K,L,matwid);  
% CONSTRAINT 4
%[C_4,bi4] = C4(R,K,L,matwid);
% CONSTRAINT 5
%[C_5,bi5] = C5(R,K,L,matwid);
% CONSTRAINT 6
%[C_6,bi6] = C6(R,K,M,L,matwid); 
% CONSTRAINT 7
%[C_7,bi7] = C7(R,K,M,L,matwid);
% CONSTRAINT 8
%[C_8,bi8] = C8(R,K,M,L,matwid); 




% Make the appropriate fillers 
%[r12,c12] = size(C_12); 
%filler12 = zeros(r12,matwid-c12); 
%[r3,c3] = size(C_3); 
%filler3 = zeros(r3,matwid - c3); 
%[r4,c4] = size(C_4); 
%filler4 = zeros(r4,matwid - c4); 
%[r5,c5] = size(C_5); 
%filler5 = zeros(r5,matwid - c5); 
%[r6,c6] = size(C_6);
%filler6 = zeros(r6,matwid - c6); 
%[r7,c7] = size(C_7); 
%filler7 = zeros(r7,matwid - c7); 
%[r8,c8] = size(C_8);
%filler8 = zeros(r8,matwid - c8);

% Filler the submatrices to hold the constraints with the proper length 
%A12 = [C_12 filler12]; 
%A3  = [C_3 filler3]; 
%A4  = [C_4 filler4];  
%A5  = [C_5 filler5];  
%A6  = [C_6 filler6]; 
%A7  = [C_7 filler7];
%A8  = [C_8 filler8]; 


% Adjust the A matrix 
%Aineq = [A12;A3;A4;A5;A6;A7;A8]; 
%bineq = [bi12;bi3;bi4;bi5;bi6;bi7;bi8];


end

