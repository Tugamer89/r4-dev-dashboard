#include <Arduino.h>

#include "DisplayEngine.h"
#include "NetworkManager.h"
#include "StateMachine.h"

// Initialize the global states
SystemMode currentMode     = SystemMode::MODE_IDLE;
CicdState currentCicdState = CicdState::UNKNOWN;

void updateState(SystemMode newMode) {
    if (currentMode != newMode) {
        currentMode = newMode;
        Serial.print("State changed to: ");
        Serial.println(static_cast<int>(currentMode));
    }
}

void updateCicdState(CicdState newState) {
    if (currentCicdState != newState) {
        currentCicdState = newState;
        Serial.print("CI/CD State changed to: ");
        Serial.println(static_cast<int>(currentCicdState));
    }
}

void setup() {
    Serial.begin(115200);
    setupDisplay();
    setupWiFi();
    Serial.println("R4 Dev Dashboard Initialized");
}

void loop() {
    // Process WiFi logic and incoming WS telemetry asynchronously
    processIncomingData();

    // Render the display based on current mode and metrics (non-blocking)
    renderDisplay();
}
