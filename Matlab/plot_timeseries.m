close all
clear all

f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\livedata\on_board_downsample_filter\7hz_calibration.txt");
data = textscan(f,'%s');
fclose(f);
data = (str2double(data{1}(2:end-1)))';

figure;
plot(1:length(data), data);
title('Time Series')

fs=64;
data_filtered = bandpass(data,[1 37],fs);

figure;
plot(1:length(data_filtered), data_filtered);
title('Time Series - Filtered')