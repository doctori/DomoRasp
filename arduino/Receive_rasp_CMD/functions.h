#include "Arduino.h"
#ifndef functions_h
#define functions_h
void doEnable(device deviceToEnable){
  digitalWrite(deviceToEnable.relay,HIGH);
}
void doDisable(device deviceToDisable){
  digitalWrite(deviceToDisable.relay,LOW);
}
#endif