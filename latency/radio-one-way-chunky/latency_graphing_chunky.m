clear;
close all;
clc;

x = (1:100);

thirtytwo = readmatrix("result-32-bytes.txt");
sixtyfour = readmatrix("result-64-bytes.txt");
onetwentyeight = readmatrix("result-128-bytes.txt");
twofiftysix = readmatrix("result-256-bytes.txt");
fivetwelve = readmatrix("result-512-bytes.txt");
tentwentyone = readmatrix("result-1021-bytes.txt");

y_thirtytwo = thirtytwo(x,2);
y_sixtyfour = sixtyfour(x,2);
y_onetwentyeight = onetwentyeight(x,2);
y_twofiftysix = twofiftysix(x,2);
y_fivetwelve = fivetwelve(x,2);
y_tentwentyone = tentwentyone(x,2);

data = [y_thirtytwo, y_sixtyfour, y_onetwentyeight, y_twofiftysix, y_fivetwelve, y_tentwentyone];

hold on;
for i = 1:width(data);
    histogram(data(:, i), "EdgeColor", "none");
end
hold off;
xlabel('latency in microseconds')
ylabel('number of samples')
leg = legend('32', '64', '128', '256', '512', '1021');
title(leg, "Message Size (bytes)");

figure;

hold on;
boxplot(data, [32, 64, 128, 256, 512, 1021]);
% boxplot(data, ["32", "64", "128", "256", "512", "1021"]);
hold off;

set(gca, 'YScale', 'log')
title('radio-one-way-chunky')
xlabel('message size (bytes)')
ylabel('latency (microseconds)')
