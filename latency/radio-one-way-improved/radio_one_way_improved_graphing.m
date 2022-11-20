clear;
x = (1:501);
result = readmatrix("result.txt");
y_result = result(x,2);
plot(y_result)
title('radio-one-way-improved')
xlabel('X')
ylabel('latency in microseconds')