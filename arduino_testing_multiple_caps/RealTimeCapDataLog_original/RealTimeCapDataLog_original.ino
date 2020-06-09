#include <Wire.h>

//AD7746 definitions
#define I2C_ADDRESS  0x48//0x90 shift one to the rigth

#define REGISTER_STATUS 0x00
#define REGISTER_CAP_DATA 0x01
#define REGISTER_VT_DATA 0x04
#define REGISTER_CAP_SETUP 0x07


#define REGISTER_VT_SETUP 0x08
#define REGISTER_EXC_SETUP 0x09
#define REGISTER_CONFIGURATION 0x0A
#define REGISTER_CAP_DAC_A 0x0B
#define REGISTER_CAP_DAC_B 0x0C
#define REGISTER_CAP_OFFSET 0x0D
#define REGISTER_CAP_GAIN 0x0F
#define REGISTER_VOLTAGE_GAIN 0x11

#define RESET_ADDRESS 0xBF

#define VALUE_UPPER_BOUND 16000000L
#define VALUE_LOWER_BOUND 0xFL
#define MAX_OUT_OF_RANGE_COUNT 3
#define CALIBRATION_INCREASE 1
byte calibration;
byte outOfRangeCount = 0;

unsigned long offset = 0;

byte data[1000];
int inst = 0;
int state = 0;
int done = 0;
int printed = 0;

void setup()
{

  pinMode(8, OUTPUT);
  pinMode(7, INPUT);

  Wire.begin(); // sets up i2c for operation
  Serial.begin(19200); // set up baud rate for serial

  Serial.println("Initializing");

  //Serial.println(readValue());

  Wire.beginTransmission(I2C_ADDRESS); // start i2c cycle
  Wire.write(RESET_ADDRESS); // reset the device
  Wire.endTransmission(); // ends i2c cycle


  //wait a tad for reboot
  delay(1);

  //Serial.println(readValue());

  writeRegister(REGISTER_EXC_SETUP, _BV(5) | _BV(3) | _BV(1) | _BV(0)); // EXC source A & B

  writeRegister(REGISTER_CAP_SETUP, _BV(7)); // cap setup reg - cap enabled

  //Serial.println("Getting offset");
  offset = ((unsigned long)readInteger(REGISTER_CAP_OFFSET)) << 8;
  //Serial.print("Factory offset: ");
  //Serial.println(offset);


  writeRegister(0x0A, _BV(7) | _BV(6) | _BV(5) | _BV(4) | _BV(3) | _BV(2) | _BV(0));  // set configuration to calib. mode, slow sample

  //wait for calibration
  delay(1);

  //displayStatus();

  //Serial.print("Calibrated offset: ");
  offset = ((unsigned long)readInteger(REGISTER_CAP_OFFSET)) << 8;
  //Serial.println(offset);
  writeRegister(REGISTER_CAP_SETUP, _BV(7)); //cin1
  //writeRegister(REGISTER_CAP_SETUP, _BV(7) | _BV(6)); // cin2, cap setup reg - cap enabled

  writeRegister(REGISTER_EXC_SETUP, _BV(5) | _BV(3)); // EXC source A & B

  // writeRegister(REGISTER_CONFIGURATION, _BV(7) | _BV(6) | _BV(5) | _BV(4) | _BV(3) | _BV(0)); // continuous mode
  writeRegister(REGISTER_CONFIGURATION, _BV(0)); //continuous, 90Hz, max filter
  
  //try cin2
  //writeRegister(REGISTER_CAP_SETUP, _BV(7) | _BV(6));
  
  calibrate();

  //displayStatus();

  //Serial.println("done");
  //Serial.println(millis());

}

void loop() // main program begins
{
  if (readValue() > 0) {
    Serial.print(readValue());
    writeRegister(REGISTER_CAP_SETUP, _BV(7) | _BV(6));
    delay(30);
    Serial.print("\t");
    Serial.println(readValue());
    writeRegister(REGISTER_CAP_SETUP, _BV(7)); //cin1
  }
  delay(30);
  if (digitalRead(7) == HIGH) {
    //Serial.println(readValue()/100000);
    delay(10);
    digitalWrite(8, LOW);

  }
}


void calibrate() {
  calibration = 20;
  writeRegister(REGISTER_CAP_DAC_A, _BV(7) | calibration);
  delay(10);
  //writeRegister(REGISTER_CAP_DAC_B, _BV(7) | calibration);
  //delay(10);

  //Serial.println("done");
}

long readValue() {
  long ret = 0;
  uint8_t data[3];

  char status = 0;


  //gets stuck here
  //wait until a conversion is done
  while (!(status & (_BV(0) | _BV(2)))) {
    //wait for the next conversion
    status = readRegister(REGISTER_STATUS);
  }

  unsigned long value =  readLong(REGISTER_CAP_DATA);

  value >>= 8;
  //we have read one byte to much, now we have to get rid of it
  ret =  value;

  return ret;
}
