%function y=signal_reference(f, S, T, N)

% f-- the fundermental frequency
% S-- the sampling rate
% T-- the number of sampling points
% N-- the number of harmonics
f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\fs512hz_gain255_30s\10hz\10hz_LED2.txt");
data = textscan(f,'%s');
fclose(f);
data = removeDC(str2double(data{1}(2:end-1))');
figure;
plot(data)
data = bandpass(data,[1 37],512);

data = (data(1,512:1023)) / (max(data(1,512:1023)));

f = 10;
S = 512;
T = S;
N = 1;

for i=1:N
   for j=1:T
    t = j/S;
    y(2*i-1,j)=sin(2*pi*(i*f)*t);
    y(2*i,j)=cos(2*pi*(i*f)*t);
   end
end

figure;
plot(data)
hold on
plot(y')
hold on

stacked_data = [data; data];
[A,B] = canoncorr(data',y');

f = 10;
S = 512;
T = S;
N = 1;

for i=1:N
   for j=1:T
    t = j/S;
    y1(2*i-1,j)=sin(2*pi*(i*f)*t);
    y1(2*i,j)=cos(2*pi*(i*f)*t);
   end
end

[A1,B1] = canoncorr(data',y1');
