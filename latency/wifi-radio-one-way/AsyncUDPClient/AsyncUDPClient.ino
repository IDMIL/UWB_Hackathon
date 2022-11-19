#include "WiFi.h"
#include "AsyncUDP.h"

const uint8_t trigger_pin = 32;
const char * ssid = "tstick_network";
const char * password = "mappings";

AsyncUDP udp;

void setup()
{
    pinMode(trigger_pin, OUTPUT);
    Serial.begin(115200);
    Serial.println("AsyncUDPClient");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    if (WiFi.waitForConnectResult() != WL_CONNECTED) {
        Serial.println("WiFi Failed");
        while(1) {
            delay(1000);
        }
    }
    if(udp.connect(IPAddress(192,168,1,255), 1234)) {
        Serial.print("UDP connected on IP: ");
        Serial.println(WiFi.localIP());
        udp.onPacket([](AsyncUDPPacket packet) {
            digitalWrite(trigger_pin, 1);
            delay(100);
            digitalWrite(trigger_pin, 0);
            Serial.println("recvd");
        });
        udp.listen(1234);
    }
}

void loop()
{
    delay(100000);
}
