function [ rho ] = makeRho(Dk)
% ADDME
% Description:
%       The function creates a set, rho, of prbabilities. 
%       whos value sums to 1. The vector is a sorted and
%       list values ind desc. order starting with the 
%       largest elem. This is used to rep that it is more
%       probable to move to the first dest in list, and 
%       each future move is less probable. 
%       
% Inputs:
%        D   :: The total number of destinations 
%        
% Return: 
%      rho   :: Random probability vector. Composed of 
%               elements describing mobility for dest d
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% asthetics
D = length(Dk);
temp = zeros(1,D);

% chose D numbers
num = 50;
max=100; 
summ = 0;

% Iterate over the entire elements in D 
for d=1:D
    temp(d)=randi(num,1,1);
    summ = summ + temp(d);
    num = floor(num/2);
    if( d == D )        
        temp(d)= abs(summ - max);
    end
end

% Sort from smallest to largest, then flip the array 
rho = fliplr(sort(temp)); 

if (sum(rho) > 100 )
    fprintf('Sum of probabilities exceeds max (100) ')
end 

% Divide each element by 100, making the probability 0<= rho <=1 
rho = rho./100; 
 
end

