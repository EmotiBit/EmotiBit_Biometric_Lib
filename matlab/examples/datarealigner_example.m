%% Created on July 3rd by Marie-Eve Bilodeau marie-eve.bilodeau.1@etsmtl.net

close all
clear all
addpath('C:\Users\marie\Documents\Maîtrise\Emotibit\realignApp\matlab\emotibit\datarealigner')

%% Program Variables  

FLEXCOMP_TIME_SECTION = 1;      % Time section in flexcomp .txt file
FLEXCOMP_EDA_SECTION = 6;       % EDA row number in flexcomp .txt file
FLEXCOMP_PPG_SECTION = 3;       % PPG row number in flexcomp .txt file
EMOTIBIT_TIME_SECTION = 'A:A';  % Time column in emotibittibit DataParser .cvs files
EMOTIBIT_DATA_SECTION = 'H:H';  % Data column in emotibittibit DataParser .cvs files
FLEX_SR = 256;                  % Flexcomp sampling rate
MAX_DELAY = 30;                 % Maximum delay in sec to shift between Flexcomp and emotibittibit data
PPG_SUBSECTION_SIZE = 60;       % Subsection duration in sec to interpolate for PPG data
EDA_SUBSECTION_SIZE = 5*60;     % Subsection duration in sec to interpolate for EDA data


%% Main

% Get Data from Files and match means and amplitudes
[dataType,flexcompTime,flexcompData,emotibitTime, emotibitData] = getRawDataFromFile(FLEXCOMP_TIME_SECTION, FLEXCOMP_EDA_SECTION,FLEXCOMP_PPG_SECTION,EMOTIBIT_TIME_SECTION,EMOTIBIT_DATA_SECTION);  

% Remove DC and match amplitude
if dataType == 'EA'; INVERT = false ;  else;  INVERT = true; end
[flexcompTime,flexcompData,emotibitTime,emotibitData] = arrangeRawData(INVERT, flexcompTime, flexcompData, emotibitTime, emotibitData);

%Plot Raw Data
figure;
plot(flexcompTime,flexcompData);
hold on;
plot(emotibitTime, emotibitData);
sgtitle(['Raw Unaligned Emotibit ', dataType, ' and FlexComp Data']);
legend('FlexComp','Emotibit');
xlabel('time (sec)');

% Get a subsection of data and interpolate emotibittibit Data at Flexcomp frequency 
% Calculate optimal delay and realign data
if dataType == 'EA'; subsectionDuration = EDA_SUBSECTION_SIZE;  else;  subsectionDuration = PPG_SUBSECTION_SIZE; end
[delay, newFlexcompTime, newFlexcompData, alignedEmotibitTime, alignedEmotibitData] = getDelayAndAlignData(flexcompTime, flexcompData, emotibitTime, emotibitData, FLEX_SR, MAX_DELAY, subsectionDuration);

% Plot final result
figure;
plot(newFlexcompTime,newFlexcompData);
hold on;
plot(alignedEmotibitTime,alignedEmotibitData);
sgtitle(['Realigned Emotibit ', dataType, ' Data with a delay of ', num2str(delay), ' seconds']);
legend('FlexComp','Emotibit');
xlabel('time (sec)');
