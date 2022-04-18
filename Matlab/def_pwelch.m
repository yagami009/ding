f = fopen('C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\gain200\connected_close_eyes.txt');
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';
data = data(:,512:end);

[pxx,f] = pwelch(data);

plot(f,10*log10(pxx))