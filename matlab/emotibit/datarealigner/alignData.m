%% Created on July 3rd by Marie-Eve Bilodeau marie-eve.bilodeau.1@etsmtl.net
% realign data2 with a given delay
% match both waves start and stop time
function [x1,y1,x2,y2] = alignData(delay,x1,y1,x2,y2)
    
    x2 = x2+delay;
    start = max(x1(1),x2(1));
    stop = min(x1(end),x2(end));
    
    x1SubIds = find(x1>=start & x1<=stop);
    x1 = x1(x1SubIds);
    y1 = y1(x1SubIds);
    
    x2SubIds = find(x2>=start & x2<=stop);
    x2 = x2(x2SubIds);
    y2 = y2(x2SubIds);
    
end
