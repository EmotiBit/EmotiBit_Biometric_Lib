%% Created on July 3rd by Marie-Eve Bilodeau marie-eve.bilodeau.1@etsmtl.net
% Interpolare a subsection of wave 2 at wave 1 frequency and return both
% subsections
function [subX1,subY1,splineX2,splineY2] = splineSubSection(x1,y1,x2,y2,subSectionDuration)

    % Geting middle subsection
    startSection = x1(size(x1,1)/2)- subSectionDuration/2;
    stopSection = startSection+subSectionDuration;
    
    x1SubIds = find(x1>=startSection & x1<=stopSection);
    subX1 = x1(x1SubIds);
    subY1 = y1(x1SubIds);

    x2SubIds = find(x2>=startSection & x2<=stopSection);
    subX2 = x2(x2SubIds);
    subY2 = y2(x2SubIds);
    
    % Applying spline to Emotibit Data at FlexComp sampling rate
    splineX2 = subX1;
    splineY2 = spline(subX2,subY2,splineX2);
    
%     figure
%     sgtitle('Sub Section and Spline Data');
%     plot(subX1,subY1);
%     hold on;
%     plot(splineX2,splineY2);

end
