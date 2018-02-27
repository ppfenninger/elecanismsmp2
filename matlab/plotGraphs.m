test = csvread('wallMotor1.csv');

time = test(:, 2);
startTime = time(1);
time = time - startTime; 
time = 256.*time./16000000;
motor = test(:, 4);
angle = test(:, 1); 

maxValue = 3*2^14;
% angle = (2*pi*angle./maxValue);
% angle = unwrap(angle);

% angle(angle > 9000) = -50;
motor(motor > 10) = 50; 

X = ones(1,length(motor));
plot(angle, motor); 
% polarY = sqrt(time.^2+angle.^2);
% polarX = atan(time./angle);
% disp(max(motor)); 
% disp(max(angle)); 
% plot(time, motor./15, 'g');
% hold on
% ylim([0, 2]);
% xlim([2, 6]); 
% plot(time(2:end), diff(angle), 'k'); 
% 
% figure;
% plot(time(2:end), diff(angle), 'k'); 
% hold on
% plot(time, motor./15, 'g');
% xlim([2, 6]); 