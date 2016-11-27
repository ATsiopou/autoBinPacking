function [ G ] = setUpGraph(G,b,s)
% ADDME
% Description: 
%        Function to initialize the Dijkstra's shortest 
%        path graph. 
%              
% Inputs:
%        G :: The original graph 
%        b :: Vaalue to be inserted 
%        s :: source node 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if ( s== 1 )
    for i=1:size(G,1)
       for j=1: size(G,1)
           if ( G(i,j) == 0 ) 
               G(i,j) = b; 
           end 
       end 
    end
end 

if( s == 2) 
    for i =1 : size(G,1) 
        for j= 1 : size(G,1)
            if ( G(i,j) == b )
                G(i,j) = 0; 
            end 
        end 
    end 
end 


end %End the function  


