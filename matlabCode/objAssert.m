function [tf] = objAssert(K,L,R,Dk,Sr,objLength) 
% ADDME
% Description : To varify the size of the objective fucntion 
% Inputs      :
%        K   :: The total number of nodes 
%        L   :: The number of vNFs 
%        R   :: The request matrix 
%        Dk  :: The total number of destinations 
%        Sr  :: Set containing heads of the chains 
%  objLength :: obj, function length precomputed    
% Return: 
%      tf    :: True(1)/False(0) 
%               True, the numbers in the obj match their
%               projected amount. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% 1 == show output, 0 == do nothing 
debug=0; 

% Extract:  
[r,c] = size(R);  % Request Size 
D = length(Dk);   % The num of destinations 
S = length(Sr);   % The number of candiadate nodes for heads 
M=K;              % This is to preserve the problems integrity.

% Calculate the number of elements in each term 

%- The number of nodes*number of network functions) 
f1 = K*L; 
%-(nOfReqsts * nOfNodes * nOfDsts * nOfHeadNodes *nOfFun) 
f2 = r*K*D*S*L; 
%-(nOfReqsts * nOfNodes * nOfDsts * nOfHeadNds *nOfFun * nOfNds*nOfFns * nOfFn-1) 
f3 = r*K*D*S*L*M*L*(L-1);
%-(nOfReqsts * nOfNodes * nOfDests * nOfHeadNds *nOfFns) 
f4 = r*K*D*S*L;

% the length of the objective function vector
sum = f1+f2+f3+f4;

if(debug)
    fprintf('Term 1: %d\n', f1)
    fprintf('Term 2: %d\n', f2)
    fprintf('Term 3: %d\n', f3)
    fprintf('Term 4: %d\n', f4)
    fprintf('Total Length: %d\n', sum)
end

% This verifies the length 
if(objLength ~= sum) 
    tf = 0;
else 
    tf = 1;
end 

end 