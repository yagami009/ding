f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\livedata\on_board_downsample_filter1\12hz_calibration.txt");
data = textscan(f,'%s');
fclose(f);
x = removeDC(str2double(data{1}(2:end-1)))';

fs=256;

x = bandpass(x,[1 32],fs);


figure;
spectrogram(x,[],[],[],fs,'yaxis','MinThreshold',10);
ylim([5 20]);