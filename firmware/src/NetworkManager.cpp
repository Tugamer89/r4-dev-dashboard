#include "NetworkManager.h"

#include <Arduino.h>
#include <ArduinoJson.h>
#include <WebSocketsClient.h>

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
const unsigned long networkInterval = 5000;  // 5 seconds retry interval
bool isWiFiConnected                = false;

WebSocketsClient wsClient;

void webSocketEvent(WStype_t type, uint8_t* payload, size_t length) {
    if (type == WStype_TEXT) {
        JsonDocument doc;
        DeserializationError error = deserializeJson(doc, payload);

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

        // CPU and RAM metrics extraction
        if (doc["cpu"].is<float>() && doc["ram"].is<float>() && doc["gpu"].is<float>()) {
            float cpu = doc["cpu"];
            float ram = doc["ram"];
            float gpu = doc["gpu"];
            updateMetrics(cpu, ram, gpu);
        }

    } else if (type == WStype_CONNECTED) {
        Serial.println("WebSocket Connected!");
    } else if (type == WStype_DISCONNECTED) {
        Serial.println("WebSocket Disconnected. Reconnecting...");
    }
}

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

    // Block until the initial connection is established to ensure stability
    while (WiFi.status() != WL_CONNECTED) {
        WiFi.begin(WIFI_SSID, WIFI_PASS);
        delay(1500);
        Serial.print(".");
    }
    Serial.println("\nWiFi Connected Successfully!");
    isWiFiConnected = true;

    // Configure WebSocket Client
    Serial.print("Starting WS Client to ws://");
    Serial.print(WS_SERVER_IP);
    Serial.print(":");
    Serial.println(WS_SERVER_PORT);

    wsClient.begin(WS_SERVER_IP, WS_SERVER_PORT, "/");
    wsClient.onEvent(webSocketEvent);
    wsClient.setReconnectInterval(5000);  // Library handles auto-reconnect natively
}

void processIncomingData() {
    // Maintain WiFi Connection
    if (WiFi.status() != WL_CONNECTED) {
        isWiFiConnected = false;

        unsigned long currentMillis = millis();
        if (currentMillis - lastNetworkAttempt >= networkInterval || lastNetworkAttempt == 0) {
            lastNetworkAttempt = currentMillis;
            Serial.println("Connection lost. Reconnecting to WiFi...");
            WiFi.begin(WIFI_SSID, WIFI_PASS);
        }
        return;  // Skip WS processing if we don't have WiFi
    }

    if (!isWiFiConnected) {
        Serial.println("WiFi Reconnected!");
        isWiFiConnected = true;
    }

    // Keep WebSocket connection alive and process incoming real-time payloads
    wsClient.loop();
}
