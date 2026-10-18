#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

enum class SystemMode { MODE_IDLE, MODE_BUILD, MODE_CICD };

extern SystemMode currentMode;

void updateState(SystemMode newMode);

#endif  // STATE_MACHINE_H
