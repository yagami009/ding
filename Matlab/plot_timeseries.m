close all
clear all

f = fopen('C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\saved_array.txt');
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';

figure;
plot(1:length(data), data);
title('Time Series')