function [ L ] = listDijkstra( L, W,s, d)
% ADDME
% Description:
%        List the shortest paths 
% Inputs:
%        L   :: Graph to be returned 
%        W   :: The 
%        s   :: The source node 
%        d   :: The destination node 
%
% Return:
%        L   :: 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


index=size(W,1);

while index>0
    if W(2,d)==W(size(W,1),d)
        L=[L s];
        index=0;
    else
        index2=size(W,1);
        while index2>0
            if W(index2,d)<W(index2-1,d)
                L=[L W(index2,1)];
                L=listDijkstra(L,W,s,W(index2,1));
                index2=0;
            else
                index2=index2-1;
            end
            index=0;
        end
    end
end

end

