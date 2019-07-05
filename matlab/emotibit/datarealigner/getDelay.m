%% Created on July 3rd by Marie-Eve Bilodeau marie-eve.bilodeau.1@etsmtl.net
% Find optimal positive or negative delay
% return delay in seconds
function delay = getDelay(y1,y2, sRate, maxDelayInSec)

    [corrNeg, idNeg] = getDelayCorr(y1,y2,sRate*maxDelayInSec);
    [corrPos, idPos] = getDelayCorr(y2,y1,sRate*maxDelayInSec);

    [val,id]=max([corrNeg,corrPos]);

    if id == 1
        % y 2 needs to be moved backward
        delay = -idNeg/sRate;
    else
        % y 2 needs to be moved foward
        delay = idPos/sRate;
    end

end
