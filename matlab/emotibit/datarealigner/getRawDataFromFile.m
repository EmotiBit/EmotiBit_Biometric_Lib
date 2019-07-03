%% Created on July 3rd by Marie-Eve Bilodeau marie-eve.bilodeau.1@etsmtl.net
% Get raw data from Flexcomp .txt file and Emotibit parser .cvs file
function [DataType,FCompTime,FCompData,EmoTime,EmoData] = getRawDataFromFile(FCompTimeSection,FCompEDASection,FCompPPGSection,EmoTimeSection,EmoDataSection)

    % Get Datatype
    prompt = ['What type of Emotibit Sensor Data will you realign ? (EA/PG/PR/PI)' '\n'];
    DataType = input(prompt,'s');
    if ~ismember(DataType,{'EA','PG','PR','PI'})
        error('Please select between EA/PG/PR/PI');
    end
    
    % Get FlexComp Data
    disp('Please select FlexComp File : ');
    [FCompFileGolden,FCompPath] = uigetfile('*.txt');
    if isequal(FCompFileGolden,0)
       error('User selected Cancel');
    else
       disp(['User selected FlexComp file : ', fullfile(FCompPath,FCompFileGolden)]);
    end

    FlexCompFile = [FCompPath 'copy.txt'];
    copyfile([FCompPath FCompFileGolden],FlexCompFile)
    % Change commas for point to be able to read floats
    file    = memmapfile(FlexCompFile, 'writable', true );
    comma   = ',';
    point   = '.';
    file.Data( transpose( file.Data==comma) ) = point;
    clear file;
    
   % Create FlexComp  matrix
    FCompMatrix= readmatrix(FlexCompFile);
    delete(FlexCompFile);
    FCompTime = FCompMatrix(2:end,FCompTimeSection);

    if DataType == 'EA'
        FCompData = FCompMatrix(2:end,FCompEDASection);
    else
        FCompData = FCompMatrix(2:end,FCompPPGSection);
    end
   
    % Get Emotibit Data
    disp(['Please select Emotibit ' DataType ' File : '] );
    [EmoFile,EmoPath]  = uigetfile('*.csv');
    if isequal(EmoFile,0)
       disp('User selected Cancel');
    else
       disp(['User selected Emotibit file : ', fullfile(EmoPath,EmoFile)]);
    end
    EmoFile = [EmoPath EmoFile];

    % Create Emotibit matrix
    EmoData = readmatrix(EmoFile,'Range', EmoDataSection);
    EmoTime = readmatrix(EmoFile,'Range', EmoTimeSection);
    EmoTime = EmoTime - floor(EmoTime(1));

end

