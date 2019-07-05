%% Created on July 3rd by Marie-Eve Bilodeau marie-eve.bilodeau.1@etsmtl.net
% Remove DC from signals and match amplitudes
function [x1,y1,x2,y2] = arrangeRawData(invert,x1,y1,x2,y2)
 
    % removing DC
    y1 = y1-mean(y1);
    y2 = y2-mean(y2);
    
    % taking middle 1/3 of the data to get peak2peak amplitude without the first artifacts 
    third = (x2(end) - x2(1))/3;
    x2SubIds = find(x2>=third & x2<=(x2(end)-third));
    y2MaxAmp = max(y2(x2SubIds))-min(y2(x2SubIds));
    x1SubIds = find(x1>=third & x1<=(x1(end)-third));
    y1MaxAmp = max(y1(x1SubIds))-min(y1(x1SubIds));
    
    % Mathcing Emotibit amplitude to FlexComp
    y2= y2/(y2MaxAmp/y1MaxAmp);
    
    % Inverting Emotibit PPG data
    if invert
        y2 = -y2;
    end

%     figure
%     sgtitle('Raw Data');
%     plot(x1,y1);
%     hold on;
%     plot(x2,y2);
     
end
