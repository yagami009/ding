
f = fopen("/Users/rishil/Desktop/FYP/EEG-decoding/unfilt.txt");
data = textscan(f,'%s');
fclose(f);
data = removeDC(str2double(data{1}(2:end-1))');

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
subplot(3,1,1)
plot(f,P1) 
title('FFT - Unfiltered')
xlabel('f (Hz)')
ylabel('|P1(f)|')
xlim([0 80])

f = fopen("/Users/rishil/Desktop/FYP/EEG-decoding/filtboard.txt");
data = textscan(f,'%s');
data = str2double(data{1}(2:end-1))';
fclose(f);

Fs = 256;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(data);     % Length of signal
t = (0:L-1)*T;        % Time vector

hold on;
s_fft = fft(data);
P2 = abs(s_fft/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
subplot(3,1,2)
plot(f,P1) 
title('FFT - Filtered using board')
xlabel('f (Hz)')
ylabel('|P1(f)|')
xlim([0 80])
ylim([0 50])


f = fopen("/Users/rishil/Desktop/FYP/EEG-decoding/filtscipy.txt");
data = textscan(f,'%s');
data = str2double(data{1}(2:end-1))';
fclose(f);

Fs = 256;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(data);     % Length of signal
t = (0:L-1)*T;        % Time vector

hold on;
s_fft = fft(data);
P2 = abs(s_fft/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
subplot(3,1,3)
plot(f,P1) 
title('FFT - Filtered using scipy')
xlabel('f (Hz)')
ylabel('|P1(f)|')
xlim([0 80])
ylim([0 50])