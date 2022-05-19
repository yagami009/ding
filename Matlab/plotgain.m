
adjustables = 0:1:255;
gains = [];
for i = 1:length(adjustables)
    valrwb = adjustables(i)*10/256 + 0.06;
    valrwa = (256 - adjustables(i))*10/256 + 0.06;
    gain = (8.2+valrwb)/(1+valrwa)+1;
    gains = [gains gain];
end

figure;
plot(adjustables, gains)
xlim([0 258])
ylim([1 19])
xlabel('Gain setting value')
ylabel('Gain')
