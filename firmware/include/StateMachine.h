#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

enum class SystemMode { MODE_IDLE, MODE_BUILD, MODE_CICD };
enum class CicdState { UNKNOWN, IN_PROGRESS, SUCCESS, FAILURE };

extern SystemMode currentMode;
extern CicdState currentCicdState;

void updateState(SystemMode newMode);
void updateCicdState(CicdState newState);

#endif  // STATE_MACHINE_H
