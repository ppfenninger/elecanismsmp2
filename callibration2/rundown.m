M = csvread('document.csv');
time = M(3907:end, 2);
angle = M(3907:end, 1);
% plot(M(:, 2))
maxValue = max(angle);
angle = 2*pi*angle./maxValue;
angle = unwrap(angle);

startTime = time(1);
time = time - startTime; 
time = 256.*time./16000000;
% speed = diff(angle)./diff(time); 
% filter = butter(2, .05);
xq = linspace(0, max(time), 500); 
betterAngle = spline(time, angle, xq);
speed = diff(betterAngle)./diff(xq); 
speed = medfilt1(speed);
xq = xq(2:end); 
plot(xq, speed, '.');
hold on
x = linspace(0, 12);
y = 772.6.*exp(-0.1953.*x); 
plot(x, y);
xlabel('time (seconds)');
ylabel('speed (radians/second)'); 
% 
% angle = [0, 45/2, 45, 45 + 45/2, 90, 90 + 45/2, 135, 135 + 45/2, 180, 180 + 45/2, 225, 225 + 45/2, 270, 270 + 45/2, 315, 315 + 45/2, 360];
% value = [2983, 16312, 13710, 10032, 7923, 4440, 656, 14943, 11326, 8155, 5832, 1852, 15693, 12756, 9253, 7062, 2920];
% hold on
% plot(angle, value, '*');
% plot(angle, value)
% xlabel('angle (degrees)');
% ylabel('encoder value'); 