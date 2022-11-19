#include <iostream>

constexpr uint8_t start_pin = 18;
constexpr uint8_t stop_pin = 23;

void setup()
{
    pinMode(start_pin, OUTPUT);
    pinMode(stop_pin, INPUT);
}

void loop()
{
    static uint64_t count = 0;
    std::cout << count << ": ";

    digitalWrite(start_pin, 1);

    unsigned long start_time = micros();
    while(!digitalRead(stop_pin)) {}
    unsigned long stop_time = micros();

    digitalWrite(start_pin, 0);

    std::cout << stop_time - start_time << std::endl;
    ++count;
    delay(1000);
}
