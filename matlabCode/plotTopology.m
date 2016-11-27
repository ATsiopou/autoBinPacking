function plotTopology(G,nAccessRouter,nGateway,rute,rutePr)
%ADDME 
% Description : 
%       Plots the topology, and all routes to AR        
% Terms:
%
%       k :: represents the node 
%       L :: Total number of functions 
%       R :: Request vector 
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% The dimensions of G - they are: [n,m] = size(G-1) 
n = length(G);    
% Get the dimentions of the matrix rute 
[row,col] = size(rute); 
% Create a color set, this depends on the number of flows (row) 
if(rutePr == 1) 
    color = {'lightseagreen','blue4','darkgreen','royalblue4'};
    setLineStyle = 'solid';  
else 
    color = {'lightseagreen','blue4','darkgreen','royalblue4'};
    setLineStyle = 'dashed'; 
end 



% node labels, these must be unique
%Alphabet = ('A':'Z').';      % Create the cell array of of nodes from A -> Z 
Alphabet = (1:n); 
Alphabet = Alphabet(1:n);

% Use the first if using characters for nodes , second for nums 
nodes = (Alphabet');  
%nodes = strvcat(Alphabet');

% get the start and end node 
startNode = nodes(1); 
if(nAccessRouter == 1)    
    endNode1 = nodes(n);
    endNode2 = 0; 
    endNode3 = 0; 
    endNode4 = 0; 
    endNode5 = 0; 
elseif(nAccessRouter == 2)
    endNode1 = nodes(n); 
    endNode2 = nodes(n-1);
    endNode3 = 0; 
    endNode4 = 0;
    endNode5 = 0; 
elseif(nAccessRouter == 3)
    endNode1 = nodes(n); 
    endNode2 = nodes(n-1);
    endNode3 = nodes(n-2); 
    endNode4 = 0; 
    endNode5 = 0; 
elseif(nAccessRouter == 4)
    endNode1 = nodes(n); 
    endNode2 = nodes(n-1);
    endNode3 = nodes(n-2);
    endNode4 = nodes(n-3); 
    endNode5 = 0; 
elseif(nAccessRouter == 5)
    endNode1 = nodes(n); 
    endNode2 = nodes(n-1);
    endNode3 = nodes(n-2); 
    endNode4 = nodes(n-3); 
    endNode5 = nodes(n-4); 
end 

% Make sure the size is correct 
%assert(all(size(G) == n)); 

% open,print the relation,close file 
%fid = fopen('/home/gaia/Documents/MATLAB/Publication1/mCode/Images/top.dot','w');
%fid = fopen('/media/gaia/69A92292134D62A0/mCode2/images/top.dot','w');
fid = fopen('/media/hermes/69A92292134D62A0/mCode2/images/top.dot','w');

fprintf(fid, 'graph G {\n');
fprintf(fid, 'overlap = false;\n');
fprintf(fid, 'center = true;\n');
fprintf(fid, 'node [color=Black]; \n'); 
for i = 1:n
    for j = i:n
        if G(i,j)
            % two if statements to check if the entrance and exit
            if(nodes(i) == startNode)
                fprintf(fid,'{node [color=Green, style=bold]; %d;}\n',nodes(i));
            end            
            if(nodes(j) == endNode1 || nodes(j) == endNode2 || ...
               nodes(j) == endNode3 || nodes(j) == endNode4 || ... 
               nodes(j) == endNode5 )
           
                fprintf(fid,'{node [color=Red, style=bold]; %d;}\n',nodes(j));
            end
           
            setCol = 'black';  
            fprintf(fid, '    %d -- %d [label="%d",color=%s, fontsize = 9] ; \n', nodes(i), nodes(j),full(G(i,j)),setCol);  
        end
        
    end
end

%--------------------%
% Draw Routes        %
%--------------------%
% Cheack if we are drawing the topology with or w/o rutes 
if(rute == 0)
    
    fprintf(fid, '}\n');
    fclose(fid);

else
    
    % Initialize jj
    jj = 0; 
    
    % Draw the routes for each path
    for i=1:row 
        % Assign a row of matrix of paths to variable r
        r = rute(i,:); 
        % Check to see if any of the values in r vec are == 0 
        len = length(r); 
       
        % Check for the 0's in the vector r. 
        countO = 0; 
        for ll = 1:len
            if(r(ll) ==0) 
                countO = countO+1; 
            end 
        end
        
        % Now take away the zeros from end-count
        r = [r(1:len-countO)];     
        len = length(r); 
        
        % Assign a different color to each flow
        setCol = color{1,i}; 
        for ii=1:len  
            jj = ii+1;
            
            fprintf(fid, '    %d -- %d [color=%s, dir=forward, style=%s] ; \n', r(ii), r(jj),setCol,setLineStyle);  

            if(jj>=len)
                break; 
            end

        end
    end 

    fprintf(fid, '}\n');
    fclose(fid);
end
% render dot file
%system('neato -Tpng /media/gaia/69A92292134D62A0/mCode2/images/top.dot -o /media/gaia/69A92292134D62A0/mCode2/images/top.png');
system('neato -Tpng /media/hermes/69A92292134D62A0/mCode2/images/top.dot -o /media/hermes/69A92292134D62A0/mCode2/images/top.png');


% Figure 
figure; 
%[img,map] = imread('/media/gaia/69A92292134D62A0/mCode2/images/top.png','png'); 
[img,map] = imread('/media/hermes/69A92292134D62A0/mCode2/images/top.png','png'); 
imshow(img,map); 


end 
