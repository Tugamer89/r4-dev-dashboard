#include "NetworkManager.h"

#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFiUdp.h>

#include "DisplayEngine.h"
#include "StateMachine.h"
#include "WiFiS3.h"

// Fallbacks
#ifndef WIFI_SSID
#define WIFI_SSID "DUMMY_SSID"
#endif

#ifndef WIFI_PASS
#define WIFI_PASS "DUMMY_PASS"
#endif

#ifndef WS_SERVER_IP
#define WS_SERVER_IP "127.0.0.1"
#endif

#ifndef WS_SERVER_PORT
#define WS_SERVER_PORT 8765
#endif

unsigned long lastNetworkAttempt    = 0;
const unsigned long networkInterval = 10000;  // 10 seconds retry interval
bool isWiFiConnected                = false;

WiFiUDP udp;
unsigned long lastPingTime       = 0;
const unsigned long pingInterval = 2000;  // Ping Python server every 2 seconds

void setupWiFi() {
    Serial.println("Initializing WiFi module...");
    if (WiFi.status() == WL_NO_MODULE) {
        Serial.println("Communication with WiFi module failed!");
        while (true) {
            yield();  // Halt execution safely
        }
    }

    Serial.print("Connecting to WiFi: ");
    Serial.println(WIFI_SSID);

    // Always disconnect first to clear the ESP32 state machine
    WiFi.disconnect();
    delay(100);
    WiFi.begin(WIFI_SSID, WIFI_PASS);

    unsigned long startAttemptTime = millis();

    // Block until the initial connection is established to ensure stability
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        if (millis() - startAttemptTime > networkInterval) {
            Serial.println("\nRetrying connection...");
            WiFi.disconnect();  // Clear stuck state before retrying
            delay(100);
            WiFi.begin(WIFI_SSID, WIFI_PASS);
            startAttemptTime = millis();
        }
    }

    Serial.println("\nWiFi Connected Successfully!");
    isWiFiConnected = true;

    // Configure UDP Client
    udp.begin(WS_SERVER_PORT);
    Serial.println("UDP listening and ready to send pings.");
}

void processIncomingData() {
    // Maintain WiFi Connection
    if (WiFi.status() != WL_CONNECTED) {
        isWiFiConnected             = false;
        unsigned long currentMillis = millis();

        if (currentMillis - lastNetworkAttempt >= networkInterval || lastNetworkAttempt == 0) {
            lastNetworkAttempt = currentMillis;
            Serial.println("Connection lost. Reconnecting to WiFi...");
            WiFi.disconnect();  // Reset the WiFi state machine
            delay(100);
            WiFi.begin(WIFI_SSID, WIFI_PASS);
        }
        return;  // Skip UDP processing if we don't have WiFi
    }

    if (!isWiFiConnected) {
        Serial.println("WiFi Reconnected!");
        isWiFiConnected = true;
        udp.begin(WS_SERVER_PORT);  // Restart UDP listening
    }

    unsigned long currentMillis = millis();
    if (currentMillis - lastPingTime >= pingInterval) {
        lastPingTime = currentMillis;
        // Send a lightweight ping to the Python server to register our IP
        udp.beginPacket(WS_SERVER_IP, WS_SERVER_PORT);
        udp.write((const uint8_t*)"PING", 4);
        udp.endPacket();
    }

    int packetSize = udp.parsePacket();
    if (packetSize) {
        char packetBuffer[512];
        int len = udp.read(packetBuffer, sizeof(packetBuffer) - 1);
        if (len > 0) {
            packetBuffer[len] = 0;  // Null terminate the string
        }

        JsonDocument doc;
        DeserializationError error = deserializeJson(doc, packetBuffer);

        if (error) {
            Serial.print("JSON Parse Failed: ");
            Serial.println(error.c_str());
            return;
        }

        const char* mode = doc["mode"];
        if (mode) {
            if (strcmp(mode, "idle") == 0) {
                updateState(SystemMode::MODE_IDLE);
            } else if (strcmp(mode, "build") == 0) {
                updateState(SystemMode::MODE_BUILD);
            } else if (strcmp(mode, "cicd") == 0) {
                updateState(SystemMode::MODE_CICD);
            }
        }

        const char* cicd_state = doc["cicd_state"];
        if (cicd_state) {
            if (strcmp(cicd_state, "in_progress") == 0) {
                updateCicdState(CicdState::IN_PROGRESS);
            } else if (strcmp(cicd_state, "success") == 0) {
                updateCicdState(CicdState::SUCCESS);
            } else if (strcmp(cicd_state, "failure") == 0) {
                updateCicdState(CicdState::FAILURE);
            } else {
                updateCicdState(CicdState::UNKNOWN);
            }
        }

        // CPU and RAM metrics extraction
        if (doc["cpu"].is<float>() && doc["ram"].is<float>() && doc["gpu"].is<float>()) {
            float cpu = doc["cpu"];
            float ram = doc["ram"];
            float gpu = doc["gpu"];
            updateMetrics(cpu, ram, gpu);
        }
    }
}
