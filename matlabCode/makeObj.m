function [ obj,f1, f2, f3, f4 ] = makeObj(K,L,R,P,V,C,Dk,Sr,rho)
% ADDME
% Description:
%       Function to create the objective function.
%       Due to the size of the obj function, it will
%       be constructed in parts, each part representing
%       the sum terms.
%
% Inputs:
%        R   :: The request matrix
%        D   :: The total number of destinations
%        K   :: The total number of nodes
%        M   :: The total number of nodes
%        L   :: Set of vNF,
%        F   :: Set containing the functions
%        Sr  :: Set of starting nodes of each chain 
%        u   :: vecotr of vNF typ i requirements 
%
% Return:
%      obj   :: The composition of each summation term
%               in the objective function.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Debug perposes 
debug = 0;  

% Get the size of the request
[row,col] = size(R);
S = length(Sr);
M = K;
D = length(Dk);
Ln=length(L); % The final value of L

% Allocate vector size
f1=zeros(K,L);
f2=zeros(row,S,D,K,L);
f3=zeros(row,S,D,K,M,L,L,L-1);
f4=zeros(row,S,D,K,L);

% The first term
for kk = 1 : K
    for ii = 1 : L
        f1(kk,ii) = C(kk,ii);
    end
end

% Second term
for rr=1: row
    for ss=1: S
        for dd=1: D
            for kk=1: K
                for ii=1: L
                    f2(rr,ss,dd,kk,ii)=rho(dd)*P(ss,kk)*V(rr,ii,1);
                end
            end
        end
    end
end

% Third term
for rr=1 : row
    for ss=1 : S
        for dd=1 : D
            for kk=1 : K
                for mm=1 : M
                    for ii=1 : L
                        for jj=1: L
                            for ll=1:L-1
                                f3(rr,ss,dd,kk,mm,ii,jj,ll)=rho(dd)*P(kk,mm)*V(rr,ii,ll)*V(rr,ii,ll+1);
                            end
                        end
                    end
                end
            end
        end
    end
end

% Fourth term
for rr=1 : row
    for ss=1 : S
        for dd=1 : D
            for kk=1 : K
                for ii=1 : L
                    f4(rr,ss,dd,kk,ii)=rho(dd)*P(ss,kk)*V(rr,ii,Ln);
                end
            end
        end
    end
end


obj = [f1(:);f2(:);f3(:);f4(:)]';        

if(debug) 
    fprintf('In makeObjective: ') 
    fprintf('Length: %d\n', length(obj)) 
end 


end

