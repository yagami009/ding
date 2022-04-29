%%Initial Conditions
zeta = 0.05;
r = 0.3;
naturalfreq = 3.198;
dampfreq = 3.194;
phi = 0.033;
X = 0.048;
omega = 0.96;
Xinitial = 0.048;
phizero = 0.0599;
%%Inputting time
idx=1;
time = [1:.01:4];
for t = time
    transient(idx) = Xinitial*exp(-zeta*naturalfreq*t)*cos((dampfreq*t)-phizero);
    steadystate(idx) = X*cos((omega*t)-phi);
    total(idx) = Xinitial*exp(-zeta*naturalfreq*t)*cos((dampfreq*t)-phizero) + X*cos((omega*t)-phi);
    idx=idx+1;
end
%%Plot
plot(time,transient,'k');
hold on
plot(time,steadystate,'b');
hold on
plot(time,total,'r');
legend('Transient','Steady State','Total');
xlabel('Time');
ylabel('Response');
title('Case I');