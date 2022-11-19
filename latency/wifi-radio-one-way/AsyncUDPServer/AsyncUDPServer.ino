#include "WiFi.h"
#include "AsyncUDP.h"

const uint8_t trigger_pin = 32;
const char * ssid = "tstick_network";
const char * password = "mappings";

AsyncUDP udp;

void setup()
{
    pinMode(trigger_pin, INPUT);
    Serial.begin(115200);
    Serial.println("AsyncUDPServer");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    if (WiFi.waitForConnectResult() != WL_CONNECTED) {
        Serial.println("WiFi Failed");
        while(1) {
            delay(1000);
        }
    }
    if(udp.listen(1234)) {
        Serial.print("UDP Listening on IP: ");
        Serial.println(WiFi.localIP());
        udp.onPacket([](AsyncUDPPacket packet) {
            Serial.print("UDP Packet Type: ");
            Serial.print(packet.isBroadcast()?"Broadcast":packet.isMulticast()?"Multicast":"Unicast");
            Serial.print(", From: ");
            Serial.print(packet.remoteIP());
            Serial.print(":");
            Serial.print(packet.remotePort());
            Serial.print(", To: ");
            Serial.print(packet.localIP());
            Serial.print(":");
            Serial.print(packet.localPort());
            Serial.print(", Length: ");
            Serial.print(packet.length());
            Serial.print(", Data: ");
            Serial.write(packet.data(), packet.length());
            Serial.println();
            //reply to the client
            packet.printf("Got %u bytes of data", packet.length());
        });
    }
}

const uint8_t msg[] = {'!'};

void loop()
{
    while (!digitalRead(trigger_pin)) {}
    size_t len_written = udp.writeTo(msg, 1, IPAddress(192,168,1,255), 1234);
    Serial.print("sent "); Serial.println(len_written);
    delay(250);
}
