f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\OC10.txt");
data = textscan(f,'%s');
fclose(f);
x = removeDC(str2double(data{1}(2:end-1)))';

fs=256;

x = bandpass(x,[1 32],fs);


figure;
spectrogram(x,[],[],[],fs,'yaxis','MinThreshold',20);
ylim([8 12])