function f = perform(funcName,title,xTitle,yTitle,data1,data2,data3)
% ADDME
% Description:
%       This is a function library workaround. Each
%       The functions implemented are used as utility 
%       functions in support of the algorithm 
% Inputs:
%       func :: function name to be executed 
%       x    :: list of arguments 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

switch(funcName)
    case 'singlePlot'
        if(data3 == 0)
            f = plot(title,xTitle,yTitle,data1,data2);
        else
            f = plot(title,xTitle,yTitle,data1,data2,data3);
        end
    case 'boxplot'
        if (data3 == 0)
            f = bxplot(title,xTitle,yTitle,data1,data2);
        else
            f = bxplot(title,xTitle,yTitle,data1,data2,data3);
        end
    case 'f3'
        f = (x);
    case 'f4'
        f = f4(x);
    case 'f5'
        f = f5(x);
    otherwise
        error(['Unknown function ', funcName]);
end


%Implementation 




end 