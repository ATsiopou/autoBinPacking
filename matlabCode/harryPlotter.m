function harryPlotter(type,data1,data2,data3,xyTitle,xLabel,yLabel)
%ADD ME 
% Description: plotter function with some wrappers 
% Inputs:  
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%======================================================%
%=                   HELPER FNs                       =%
%======================================================%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : setTitle()
% Decr     : Set the title as a string
% Input    :
%     t   :: The title as a string
% Return   :
%   ttl   :: Vector containing destination nodes.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [ ttl ] = setTitle(t)
        ttl = t;
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : setxLabel
% Decr     : Set the title as a string
% Input    :
%     t   :: The title as a string
% Return   :
%   ttl   :: Vector containing destination nodes.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [ xlbl ] = setxLabel(xLabel)
        xlbl = xLabel;
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : setxLabel
% Decr     : Set the title as a string
% Input    :
%     t   :: The title as a string
% Return   :
%   ttl   :: Vector containing destination nodes.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [ ylbl ] = setyLabel(yLabel)
        ylbl = yLabel;
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Func     : makeplot()
% Decr     : plot data set(s), return the handle
% Input    :
% data1/2 :: The data to be plotted
% Return   :
%   hndl  :: The plot handle
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    function [ hndl1 , hndl2 ] = makePlot(data1, data2)   
        if( data2 == 0 )
            hndl1 = plot(data1); 
            hdnl2 = 0; 
        else 
            hndl1 = plot(data1); 
            hold on; 
            hndl2 = plot(data2); 
        end
    end

%======================================================%
%=                      MAIN                          =%
%======================================================%

% Set the basic        
xyTitle=setTitle(xyTitle); 
xLabel=setxLabel(xLabel);
yLabel=setyLabel(yLabel);
fontype='Courier New';
xGridCol=[0.9 0.9 0.9];
yGridCol=[0.9 0.9 0.9];
mrkrEgdeColor1='r';
mrkrEgdeColor2='b';
mrkrEgdeColor3='g';
% Line and Marker
lineclr='black';
lwidth=1;
mrkrSize=07;
insideMrkrFaceColor=[0.5,0.5,0.5];

switch(type)
    case 1
        % xticklabels
        xticklabels = {'10', '15','20'};
        spacing= 5;
        x = 1:spacing:spacing*numel(xticklabels);
    case 2        
        % xticklabels
        xticklabels = { '5','10', '15','20'};
        spacing= 5;
        x = 1:spacing:spacing*numel(xticklabels);
   case 3
        % xticklabels
        xticklabels = { '0','0.5', '1'};
        spacing= 5;
        x = 1:spacing:spacing*numel(xticklabels);        
    otherwise
        
end

%make a new window 
figure(); 
% Plots


hP1 = plot(data1);
hold on 
hP2 = plot(data2);
hP3 = plot(data3);

%set(gca,'XTick',[0:15]) 

set(hP1, ...
    'color',lineclr, ...
    'linestyle','-', ...
    'Marker','s', ...
    'LineWidth',lwidth,...
    'MarkerSize',mrkrSize,...
    'MarkerEdgeColor',mrkrEgdeColor1,...
    'MarkerFaceColor',insideMrkrFaceColor);

set(hP2, ...
    'color',lineclr, ...
    'linestyle','-', ...
    'Marker','o', ...
    'LineWidth',lwidth,...
    'MarkerSize',mrkrSize,...
    'MarkerEdgeColor',mrkrEgdeColor2,...
    'MarkerFaceColor',insideMrkrFaceColor);

set(hP3, ...
    'color',lineclr, ...
    'linestyle','-', ...
    'Marker','x', ...
    'LineWidth',lwidth,...
    'MarkerSize',mrkrSize,...
    'MarkerEdgeColor',mrkrEgdeColor3,...
    'MarkerFaceColor',insideMrkrFaceColor);

set(gca,'XTickLabel',xticklabels,'XTick',1:spacing:spacing*numel(xticklabels));

%# Set both fontypes 
set(gca,'FontName',fontype);

%# capture handle to current figure and axis
hFig = gcf;
hAx1 = gca;

%# create a second transparent axis, as a copy of the first
hAx2 = copyobj(hAx1,hFig);
delete( get(hAx2,'Children') )
set(hAx2, 'Color','none', 'Box','off','XGrid','off', 'YGrid','off')

%# show grid-lines of first axis, style them as desired,
%# but hide its tick marks and axis labels
set(hAx1, ...
    'XColor',xGridCol, 'YColor',yGridCol, ...
    'XMinorGrid','off', 'YMinorGrid','off', 'MinorGridLineStyle','-', ...
    'XGrid','off', 'YGrid','off','GridLineStyle','-', ...
    'XTickLabel',[], 'YTickLabel',[]);

%# link the two axes to share the same limits on pan/zoom
linkaxes([hAx1 hAx2], 'xy');

%# Note that `gca==hAx1` from this point on...
%# If you want to change the axis labels, explicitly use hAx2 as parameter

%# Set the title and labels 
clear title; 
set(gca,'Title',text('String',xyTitle))
xlabel(hAx2, xLabel);
ylabel(hAx2, yLabel);


%# Set the legend 
legend([hP1 hP2 hP3], {'AGW', 'P-PCC', 'SPBA'}, 'Location', 'NorthEast');


end

