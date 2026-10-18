#ifndef DISPLAY_ENGINE_H
#define DISPLAY_ENGINE_H

#include <Arduino.h>

void setupDisplay();
void updateMetrics(float cpu, float ram, float gpu);
void renderDisplay();

#endif  // DISPLAY_ENGINE_H
