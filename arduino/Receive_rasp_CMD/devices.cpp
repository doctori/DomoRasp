/*
  Device handling for led strips
*/
#include "Arduino.h"
#include "devices.h"

Device::Device(unsigned short relay,unsigned short intensityPin){
  _relay = relay ;
  _intensityPin = intensityPin;
};
Device::Device(void){};
void Device::light(unsigned short intensity){
  analogWrite(_intensityPin, intensity);
};
unsigned short Device::getLight(){
  return static_cast<unsigned short>(analogRead(_intensityPin));
};
void Device::doEnable(){
  digitalWrite(_relay,HIGH);
};
void Device::doDisable(){
  digitalWrite(_relay,LOW);
};

DeviceRGB::DeviceRGB(unsigned short relay,unsigned short intensityPinR,unsigned short intensityPinG,unsigned short intensityPinB) : Device(relay,intensityPinR){
  _intensityPin = intensityPinR;
  _intensityPinR = intensityPinR;
  _intensityPinG = intensityPinG;
  _intensityPinB = intensityPinB;
};
DeviceRGB::DeviceRGB(void) : Device(){};

void DeviceRGB::light(unsigned short intensityR,unsigned short intensityG,unsigned short intensityB){
  printf("writting on Red : [%d] with the value %d\n",_intensityPinR,intensityR);
  analogWrite(_intensityPinR,intensityR);
  printf("writting on Green : [%d] with the value %d\n",_intensityPinG,intensityG);
  analogWrite(_intensityPinG,intensityG);
  printf("writting on Blue : [%d] with the value %d\n",_intensityPinB,intensityB);
  analogWrite(_intensityPinB,intensityB);
};
void DeviceRGB::light(unsigned short intensity){
  DeviceRGB::light(intensity,intensity,intensity);
};

