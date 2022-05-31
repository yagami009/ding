f = fopen("/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/log/OC1.txt");
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';

fs = 256;

alpha_bandpower = bandpower(data(1:length(data)/2), fs, [8 12]);
alpha_bandpower1 = bandpower(data(length(data)/2:end), fs, [8 12]);