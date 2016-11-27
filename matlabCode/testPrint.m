function  testPrint(printCase,xyTitle,xLabel,yLabel)

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

    function [agw,sbpa,ppcc,xticklabels,spacing,x] = chooseData(type)
        switch(type)
            case 1
                % K CASE
                agw  = [10.18,9.60,8.93,8.72,8.70,8.67,8.64,8.79,8.64,8.53,8.56];
                sbpa = [8.22,8.08,7.39,7.11,6.91,6.93,6.91,6.57,6.54,6.76,6.65];
                ppcc = [7.09,7.06,6.37,6.06,5.94,5.98,6.03,5.89,6.02,6.02,5.87];
                % xticklabels
                xticklabels = {'10', '15','20'};
                spacing= 5;
                x = 1:spacing:spacing*numel(xticklabels);
            case 2
                % R CASE
                agw  = [19.00,20.90,22.80,24.70,26.60,28.50,30.40,32.30,34.20,36.10,38.00];
                sbpa = [14.85,16.48,17.90,19.45,20.93,22.93,24.89,26.81,28.84,30.58,32.75];
                ppcc = [13.62,15.17,16.45,17.89,19.25,21.28,23.25,25.19,27.26,28.94,31.19];
                % xticklabels
                xticklabels = { '5','10', '15','20'};
                spacing= 5;
                x = 1:spacing:spacing*numel(xticklabels);
            case 3
                % R CASE
                agw  = [40.00,40.00,40.00,40.00,40.00,40.00,40.00,40.00,40.00,40.00,40.00];
                sbpa = [36.64,36.26,35.71,34.65,34.20,33.16,32.67,31.77,31.26,30.56,30.00];
                ppcc = [31.17,31.01,31.25,31.27,32.49,33.16,32.67,31.77,31.26,30.56,30.00];
            
                % xticklabels
                xticklabels = { '0','0.5', '1'};
                spacing= 5;
                x = 1:spacing:spacing*numel(xticklabels);
            otherwise
                
        end
        
    end 

%======================================================%
%=                      MAIN                          =%
%======================================================%


% Choose the data set we want to print 
[agw,sbpa,ppcc,xticklabels,spacing,x] = chooseData(printCase);

% Set the basic        
xyTitle=setTitle(xyTitle); 
xLabel=setxLabel(xLabel);
yLabel=setyLabel(yLabel);
fontype='Courier New';
xGridCol=[0.9 0.9 0.9];
yGridCol=[0.9 0.9 0.9];
mrkrEgdeColor1='black';
mrkrEgdeColor2='r';
mrkrEgdeColor3='b';
% Line and Marker
lineclr='black';
lwidth=1.2;
mrkrSize=05;
textLabelSize=12; 
insideMrkrFaceColor=[0.5,0.5,0.5];



%make a new window 
figure(); 
% Plots


hP1 = plot(agw);
hold on 
hP2 = plot(sbpa);
hP3 = plot(ppcc);

%set(gca,'XTick',[0:15]) 
%set(gca,fontsize,textLabelSize) 
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
    'Marker','^', ...
    'LineWidth',lwidth,...
    'MarkerSize',mrkrSize,...
    'MarkerEdgeColor',mrkrEgdeColor2,...
    'MarkerFaceColor',insideMrkrFaceColor);

set(hP3, ...
    'color',lineclr, ...
    'linestyle','-', ...
    'Marker','o', ...
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
    'XGrid','on', 'YGrid','on','GridLineStyle',':', ...
    'Xtick',1:1:numel(agw), ...
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
