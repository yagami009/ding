f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\livedata\fs64_ns256_FULLSCREEN_1\7hz_calibration.txt");
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';
data = data(:,512:end);

[pxx,f] = pwelch(data);

plot(f,10*log10(pxx))