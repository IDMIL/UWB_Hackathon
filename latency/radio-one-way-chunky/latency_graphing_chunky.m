clear;
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

plot(x,y_thirtytwo,x,y_sixtyfour,x,y_onetwentyeight,x,y_twofiftysix,x,y_fivetwelve,x,y_tentwentyone)
title('radio-one-way-chunky')
xlabel('X')
ylabel('latency in microseconds')