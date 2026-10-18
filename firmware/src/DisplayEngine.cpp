#include "DisplayEngine.h"

#include "Arduino_LED_Matrix.h"
#include "StateMachine.h"

ArduinoLEDMatrix matrix;

float currentCpu                   = 0.0;
float currentRam                   = 0.0;
float currentGpu                   = 0.0;
unsigned long lastRenderTime       = 0;
const unsigned long renderInterval = 100;  // 10 FPS rendering

void setupDisplay() {
    matrix.begin();
}

void updateMetrics(float cpu, float ram, float gpu) {
    currentCpu = cpu;
    currentRam = ram;
    currentGpu = gpu;
}

void renderIdle() {
    int cpuHeight = (int)((currentCpu / 100.0) * 8);
    int ramHeight = (int)((currentRam / 100.0) * 8);
    int gpuHeight = (int)((currentGpu / 100.0) * 8);

    uint8_t frame[8][12] = {0};

    // CPU (Left, Cols 1 and 2)
    for (int i = 0; i < cpuHeight; i++) {
        frame[7 - i][1] = 1;
        frame[7 - i][2] = 1;
    }

    // RAM (Center, Cols 5 and 6)
    for (int i = 0; i < ramHeight; i++) {
        frame[7 - i][5] = 1;
        frame[7 - i][6] = 1;
    }

    // GPU (Right, Cols 9 and 10)
    for (int i = 0; i < gpuHeight; i++) {
        frame[7 - i][9]  = 1;
        frame[7 - i][10] = 1;
    }

    matrix.renderBitmap(frame, 8, 12);
}

void renderDisplay() {
    unsigned long currentMillis = millis();

    // Non-blocking frame rate control
    if (currentMillis - lastRenderTime < renderInterval) {
        return;
    }
    lastRenderTime = currentMillis;

    // Use the globally available currentMode
    switch (currentMode) {
        case SystemMode::MODE_IDLE:
            renderIdle();
            break;
        case SystemMode::MODE_BUILD:
            // Placeholder build animation
            break;
        case SystemMode::MODE_CICD:
            // Placeholder CI/CD animation
            break;
    }
}
