f = fopen("/Users/rishil/Desktop/FYP/EEG-decoding/filtboard.txt");
data = textscan(f,'%s');
fclose(f);
data = removeDC(str2double(data{1}(2:end-1))');

figure;

plot(1:length(data), data);
title('Time Series')

y = bandpass(data,[4 28],256);

figure;
plot(1:length(y), y);
title('Time Series filtered - Bandpass 1-32hz')
ylim([-400 200])

Fs = 256;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(data);     % Length of signal
t = (0:L-1)*T;        % Time vector

figure;
s_fft = fft(data);
P2 = abs(s_fft/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('FFT - Unfiltered')
xlabel('f (Hz)')
ylabel('|P1(f)|')
ylim([0 50])


Fs = 256;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(y);     % Length of signal
t = (0:L-1)*T;        % Time vector

figure;
s_fft = fft(y);
P2 = abs(s_fft/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('FFT - Filtered')
xlabel('f (Hz)')
ylabel('|P1(f)|')
ylim([0 50])