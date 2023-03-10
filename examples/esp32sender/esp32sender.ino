/*
Stream bytes from eDVS over ESP-NOW

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include <esp_now.h>
#include <WiFi.h>

#include "edvs.h"

static const uint8_t ESP_RECEIVER_ADDRESS[] = {0xAC, 0x0B, 0xFB, 0x6F, 0x6C, 0x04};

static const uint8_t RX_PIN = 4;
static const uint8_t TX_PIN = 14;

static eDVS edvs;

static void reportForever(const char * msg)
{
    while (true) {
        Serial.println(msg);
        delay(500);
    }
}

void serialEvent1(void)
{
    while (Serial1.available()) {
        edvs.update(Serial1.read());
    }
}

void setup(void)
{
    Serial.begin(115200);

    Serial1.begin(2000000, SERIAL_8N1, RX_PIN, TX_PIN);

    edvs.begin(Serial1);

    /*
    WiFi.mode(WIFI_STA);

    if (esp_now_init() != ESP_OK) {
        reportForever("Error initializing ESP-NOW");
    }

    static esp_now_peer_info_t peerInfo;

    memcpy(peerInfo.peer_addr, ESP_RECEIVER_ADDRESS, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;

    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        reportForever("Failed to add peer");
    }*/
}

void loop(void)
{
    if (edvs.hasNext()) {

        // Display event
        eDVS::event_t e;
        edvs.next(e);

        Serial.printf("%3d %3d %c\n", e.x, e.y, e.p > 0 ? '+' : '-');
    }

     // Send message bytes directly to ESP receiver
    //esp_now_send(ESP_RECEIVER_ADDRESS, &byte, 1);
}
