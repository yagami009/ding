close all
clear all

f = fopen('/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/log/10hz1.txt');
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';

x0  = data(:);
x1  = diff([0; x0]);
x2  = diff([0; x1]);

sd0 = std(x0);
sd1 = std(x1);
sd2 = std(x2); 

hjorth_complexity  = (sd2/sd1)/(sd1/sd0);


