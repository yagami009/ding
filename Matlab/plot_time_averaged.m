clear all
close all

f = fopen('C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\gain200\connected_close_eyes.txt');
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';
data = data(:,512:end);

fs=256;
average_samples = 4;
data = data';
s1 = size(data, 1);
m  = s1 - mod(s1, average_samples);
y  = reshape(data(1:m), average_samples, []); 
averaged_samples = sum(y, 1) / average_samples;  

figure;
plot(1:length(averaged_samples), averaged_samples);
title('Averaged Time Series')