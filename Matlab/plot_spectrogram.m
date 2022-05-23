f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\fs512hz_gain255_30s\open_close\15sopen_15sclose3.txt");
data = textscan(f,'%s');
fclose(f);
x = removeDC(str2double(data{1}(2:end-1)))';

fs=512;

x = bandpass(x,[1 32],fs);


figure;
spectrogram(x,[],[],[],fs,'yaxis','MinThreshold',0);
ylim([5 20]);