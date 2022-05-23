f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\fs512hz_gain255_30s\open_close\15sopen_15sclose3.txt");
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';

figure;
data = data(:,length(data)/2:end);
%data = data(:,1:length(data)/2);

[pxx,f] = pwelch(data);

plot(f,10*log10(pxx))