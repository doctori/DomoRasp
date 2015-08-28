#ifndef device_h
#define device_h
#include "Arduino.h"

class Device {
  public:
    Device(unsigned short relay,unsigned short intensityPin);
    Device(void);
    void setIntensityPin(unsigned short intensityPin);
    unsigned short getLight();
    void doEnable();
    void doDisable();
    void light(unsigned short intensity);
  protected:
    unsigned short _relay;
    unsigned short _intensityPin;

   
  };
class DeviceRGB:public Device {
  protected:
    unsigned short _intensityPinR;
    unsigned short _intensityPinG;
    unsigned short _intensityPinB;
   public:
    DeviceRGB(unsigned short relay,unsigned short intensityPinR,unsigned short intensityPinG,unsigned short intensityPinB);
    DeviceRGB(void);
    void Green();
    void Red();
    void Blue();
    void light(unsigned short intensity);
    void light(unsigned short intensityR,unsigned short intensityG,unsigned short intensityB);
};



#endif
