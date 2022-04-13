close all
clear all

f = fopen('C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\10hz1.txt');
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';

fs = 256;
data = data(1,512:end);

% alpha (8?12 Hz)
% delta (1?4 Hz)
% theta (4?8 Hz)
% beta (13?30 Hz), 

f_alpha = [8 12];
f_beta = [13 30];
f_delta = [1 4];
f_theta = [4 8];

alpha_bandpower = bandpower(data, fs, [f_alpha(1) f_alpha(2)]);
beta_bandpower = bandpower(data, fs, [f_beta(1) f_beta(2)]);
delta_bandpower = bandpower(data, fs, [f_delta(1) f_delta(2)]);
theta_bandpower = bandpower(data, fs, [f_theta(1) f_theta(2)]);