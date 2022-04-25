f = fopen("/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/log/fs512hz_gain255_30s/10hz/10hz_LED2.txt");
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';
data_y = data(1,1024:end);
figure;

r = fopen('/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/log/fs512hz_gain255_30s/open/open_eyes.txt');
data = textscan(r,'%s');
fclose(r);
ref = str2double(data{1}(2:end-1))';
ref = ref(1,1024:end);
figure;

plot(1:length(data_y), data_y);
title('Time Series')

y = bandpass(data_y,[1 37], 512);
y_ref = bandpass(ref, [1 37], 512);
figure;
plot(1:length(y), y);
title('Data filtered')


Fs = 512;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(data);     % Length of signal
t = (0:L-1)*T;        % Time vector

figure;
s_fft = fft(y);
s_fft_ref = fft(y_ref);
s_fft = s_fft - s_fft_ref;
P2 = abs(s_fft/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of Data')
xlabel('f (Hz)')
ylabel('|P1(f)|')
ylim([0 50])