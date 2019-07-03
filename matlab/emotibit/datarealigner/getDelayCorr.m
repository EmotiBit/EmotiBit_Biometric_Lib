%% Created on July 3rd by Marie-Eve Bilodeau marie-eve.bilodeau.1@etsmtl.net
% Get optimal correlation of y1 and delayed y2
function [delayCorr, delayId] = getDelayCorr(y1,y2, maxDelay)
    step = 1:1:maxDelay;
    for n = step
        delayCorr(n) = sum(y1(1:end-n+1).*y2(n:end)); 
    end
    [delayCorr, delayId] = max(delayCorr);
end
