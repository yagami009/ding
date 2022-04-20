f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\fs512hz_gain255_30s\open_close\15sopen_15sclose1.txt");
data = textscan(f,'%s');
fclose(f);
data_noDC = removeDC(str2double(data{1}(2:end-1)))';

fs=512;
data_filtered = bandpass(data_noDC,[1 37],fs);