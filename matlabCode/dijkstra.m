function [e, L] = dijkstra(A,s,d)
%%ADDME 
% Descr : Dijkstra Algorithm
% usage:
% [cost rute] = dijkstra(Graph, source, destination)
% 
% Example : 
%
% G = [0 3 9 0 0 0 0;
%      0 0 0 7 1 0 0;
%      0 2 0 7 0 0 0;
%      0 0 0 0 0 2 8;
%      0 0 4 5 0 9 0;
%      0 0 0 0 0 0 4;
%      0 0 0 0 0 0 0;
%      ];
% [e,L] = dijkstra(G,1,7)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% If the source is equal to the destination
if (s == d)
    e=0;
    L=[s];

% If the source is different to the destination 
else 
    A = setUpGraph(A,inf,1);
    if d==1
        d=s;
    end
    
   A=exchangeNode(A,1,s);
    
    lengthA=size(A,1);
    W=zeros(lengthA);
    
    
    for i=2 : lengthA
        W(1,i)=i;
        W(2,i)=A(1,i);
    end
    
    
    
    for i=1 : lengthA
        D(i,1)=A(1,i);
        D(i,2)=i;
    end
    length(D)
    D2=D(2:length(D),:);
    L=2;
    %(size(W,1)-1)
    while L<=(size(W,1)-1)
        L=L+1;
        D2=sortrows(D2,1);
        k=D2(1,2);
        
        fprintf('--------------------\n')    
        fprintf('-       Start      -\n')    
        fprintf('--------------------\n')
        fprintf('k: %d\n',k); 
        fprintf('L: %d\n',L);
        W(L,1)=k;
        D2(1,:)=[];
        
        D2
        for i=1 : size(D2,1)
            
            fprintf('i,: %d\n',i); 
            fprintf('D2(i,2)      : %d \nD(D2(i,2):,1): %d \nA: %d\n',D2(i,2),D(D2(i,2),1), A(k,D2(i,2)) );
            fprintf('D(D2(i,2))   : %d\n',D(D2(i,2),1))
            fprintf('D(k,1)       : %d\n',D(k,1))
            fprintf('A(k,D2(i,2))): %d\n',A(k,D2(i,2)))
            fprintf('D(k,1) + A(k,D2(i,2)): %d\n',D(k,1) + A(k,D2(i,2)))
            if D(D2(i,2),1)>(D(k,1)+A(k,D2(i,2)))
                fprintf('Enter :\n')
                D(D2(i,2),1) = D(k,1)+A(k,D2(i,2));
                D2(i,1) = D(D2(i,2),1);
                fprintf('After D : %d\n',D(D2(i,2),1))
                fprintf('After D2: %d\n',D2(i,1))
            end
        end
        
        for i=2 : length(A)
            W(L,i)=D(i,1);
        end
    end
    if d==s
        L=[1];
    else
        L=[d];
    end
    e=W(size(W,1),d);
    L = listDijkstra(L,W,s,d);
end