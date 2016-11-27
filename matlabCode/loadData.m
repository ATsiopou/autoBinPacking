function [swCase,nAR,Sr,D,G,R,K,M,L,C,U,u] = loadData()
% ADDME
% Description: Loads data, prompt usr for type ret data 
% Inputs     : NONE 
% Return     :
%       nAr :: Number of access routers for graph  
%       G   :: Graph to be returned 
%       R   :: The request matrix 
%       C   :: The node cost matrix 
%       K   :: The total number of nodes 
%       M   :: The total number of nodes 
%       L   :: Set of vNF 
%       U   :: Node utility constraints  
%       u   :: vNF utility requirements 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Clear the screen 
clc; 

% Define the delimeter 
delimiterOut=' '; 
filePath='confiurationFiles/'; 

%%%    Prompt    %%%
fprintf(' Options: '); 
fprintf('\n'); 
fprintf('1) K = 6  , L = 5, R = 5 \n'); 
fprintf('2) Monte Carlo Simulation  \n'); 
fprintf('\n');
prompt1 = 'Choice: ';
p1=input(prompt1);
%%%    Configuration choice   %%%
switch(p1)
    case 1
        % Load the filenames
        fileName1 = 'configurationFiles/config1/G.conf';
        fileName2 = 'configurationFiles/config1/R.conf';
        fileName3 = 'configurationFiles/config1/c0.conf';
        fileName4 = 'configurationFiles/config1/U.conf';
        fileName5 = 'configurationFiles/config1/u.conf';
        fileName6 = 'configurationFiles/config1/Sr.conf';
        fileName7 = 'configurationFiles/config1/D.conf';
        % The number of access routers
        nAR = 3;             
        L = 5; 
        swCase = 1; 
        
    case 2  
        
        % Load Default Monte carlo Filenames
        fileName1 = 'configurationFiles/configMC/G.conf';
        fileName2 = 'configurationFiles/configMC/R.conf';
        fileName3 = 'configurationFiles/configMC/c0.conf';
        fileName4 = 'configurationFiles/configMC/U.conf';
        fileName5 = 'configurationFiles/configMC/u.conf';
        fileName6 = 'configurationFiles/configMC/Sr.conf';
        fileName7 = 'configurationFiles/configMC/D.conf';
        % The number of access routers
        nAR = 5;             
        L = 4;  
        swCase = 2; 

    otherwise
        printf(' Not a valid choice .. ');

end 


% Import the config files 
[G,delimiterOut] = importdata(fileName1);
[R,delimiterOut] = importdata(fileName2);
[C,delimiterOut] = importdata(fileName3);
[U,delimiterOut] = importdata(fileName4);
[u,delimiterOut] = importdata(fileName5);
[Sr,delimiterOut]= importdata(fileName6);
[D,delimiterOut] = importdata(fileName7);

% Get the number of nodes 
[row,c] = size(G); 
K = row - nAR;  
M = K; 

end 
