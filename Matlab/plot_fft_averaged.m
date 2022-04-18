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

Fs = 256;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(data);     % Length of signal
t = (0:L-1)*T;        % Time vector

figure;
s_fft = fft(data);
P2 = abs(s_fft/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of Data')
xlabel('f (Hz)')
ylabel('|P1(f)|')
ylim([0 12])