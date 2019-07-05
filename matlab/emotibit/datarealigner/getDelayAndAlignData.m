%% Created on July 3rd by Marie-Eve Bilodeau marie-eve.bilodeau.1@etsmtl.net
% Get a subsection of data and interpolate Emotibit Data at Flexcomp frequency 
% Calculate optimal delay and realign data
function [delay,x1,y1,x2,y2] = getDelayAndAlignData(x1, y1, x2, y2, sRate, MaxDelayInSec, subsectionDuration)
    
    [subX1,subY1,splineX2,splineY2] = splineSubSection(x1,y1,x2,y2,subsectionDuration);
    delay = getDelay(subY1, splineY2, sRate, MaxDelayInSec);
    [x1,y1,x2,y2] = alignData(delay,x1,y1,x2,y2);
    
end

