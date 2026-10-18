#include <Arduino.h>

#include "Arduino_LED_Matrix.h"
#include "StateMachine.h"

SystemMode currentMode = SystemMode::MODE_IDLE;
ArduinoLEDMatrix matrix;

unsigned long previousMillis = 0;
const long interval          = 100;  // 100ms refresh rate

void updateState(SystemMode newMode) {
    if (currentMode != newMode) {
        currentMode = newMode;
        Serial.print("State changed to: ");
        Serial.println(static_cast<int>(currentMode));
    }
}

void handleIdleMode() {
    // Render CPU/RAM telemetry histogram
}

void handleBuildMode() {
    // Render build progress animation
}

void handleCICDMode() {
    // Render CI/CD success/failure status
}

void setup() {
    Serial.begin(115200);
    matrix.begin();
    Serial.println("R4 Dev Dashboard Initialized");
}

void loop() {
    unsigned long currentMillis = millis();

    // Non-blocking timer
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;

        switch (currentMode) {
            case SystemMode::MODE_IDLE:
                handleIdleMode();
                break;
            case SystemMode::MODE_BUILD:
                handleBuildMode();
                break;
            case SystemMode::MODE_CICD:
                handleCICDMode();
                break;
        }
    }

    // Non-blocking WebSockets listener logic goes here
}
