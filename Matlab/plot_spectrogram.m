f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\saved_array.txt");
data = textscan(f,'%s');
fclose(f);
x = removeDC(str2double(data{1}(2:end-1)))';

fs=512;

x = bandpass(x,[1 37],fs);
average_samples = 4;
data = x';
s1 = size(data, 1);
m  = s1 - mod(s1, average_samples);
y  = reshape(data(1:m), average_samples, []); 
averaged_samples = sum(y, 1) / average_samples;

fs_new = 128;

figure;
spectrogram(averaged_samples,[],[],[],fs_new,'yaxis','MinThreshold',0);
ylim([5 20]);