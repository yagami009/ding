close all
clear all

f = fopen('/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/log/10hz1.txt');
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';

figure;
plot(1:length(data), data);
title('Time Series')