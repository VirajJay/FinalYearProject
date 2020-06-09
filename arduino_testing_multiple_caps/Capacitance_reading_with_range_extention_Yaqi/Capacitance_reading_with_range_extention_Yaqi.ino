#include <Wire.h>

//AD7746 definitions
#define TCAADDR 0x70
#define I2C_ADDRESS  0x48//0x90 shift one to the right

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

int cap_one=1;
int cap_two=2;

void tcaselect(uint8_t i) {
  if (i > 7) return;
 
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}


void setup_devices(int dev_num){
  tcaselect(dev_num);
  Wire.beginTransmission(I2C_ADDRESS); // start i2c cycle
  Wire.write(RESET_ADDRESS); // reset the device
  Wire.endTransmission(); // ends i2c cycle

    //wait a tad for reboot
  delay(1);

  displayStatus("PreSetup"); //We should have default reset condition.
  
  //Setup CAPDAC Registers
  writeRegister(REGISTER_CAP_SETUP,_BV(7)); // cap setup reg - cap enabled
  writeRegister(REGISTER_EXC_SETUP, _BV(5) | _BV(3) | _BV(1) | _BV(0)); // EXC A&B on


  calibrate();

  displayStatus("ChkSetup");
writeRegister(REGISTER_CONFIGURATION, _BV(0)); //continuous, 90Hz, max filter

  
  }

void setup()
{
pinMode(18, INPUT);
pinMode(19, INPUT);
 // pinMode(8, OUTPUT);
  //pinMode(7, INPUT);

  Wire.begin(); // sets up i2c for operation
  Serial.begin(19200); // set up baud rate for serial monitor

  Serial.println("\nInitializing_mds-v1");

  setup_devices(cap_one);
  setup_devices(cap_two);



}
long preval=0; //Stores previous value for filtering purposes
long capval=0;// stores current cap value
long vt_val=0;  //stores voltage temp data
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void loop() // main program begins
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
{
  tcaselect(cap_one);
  delay(1);
  capval=readCapValue(); //read cap value from registers
  delay(30);
  Serial.print(capval);  //displays in femtofarads (/1000 for PF)
  Serial.print("\n");
  preval=capval;  //save new value
  tcaselect(cap_two);
  delay(1);
  capval=readCapValue(); //read cap value from registers
  delay(30);
  Serial.print(capval);  //displays in femtofarads (/1000 for PF)
  Serial.print("\n");
  preval=capval;  //save new value
}
//~~~~~~~~~~~~~~~~~~~~~~
void calibrate() {
//~~~~~~~~~~~~~~~~~~~~~~
  calibration =127;
  writeRegister(REGISTER_CAP_DAC_A, _BV(7) | calibration);
  delay(10);
writeRegister(REGISTER_CAP_DAC_B, _BV(7) | calibration);
 delay(10);

  //Serial.println("done");
}
///~~~~~~~~~~~~~~~~~~~~~~~~~~
// Read value of capcitor
//~~~~~~~~~~~~~~~~~~~~~~~~~~~
long readCapValue() {
  long ret = 0;
  uint8_t data[3];

  char status = 0;
  //wait until a conversion is done
  while (!(status & (_BV(0) | _BV(2)))) {
    //wait for the next conversion
    status = readRegister(REGISTER_STATUS);
  }

  unsigned long value =  readLong(REGISTER_CAP_DATA); //Read "4bytes" from Cap Data register
  //readLong() reads one byte too many, we have to get rid of it
  value >>= 8;

  ret = value;
  return ret;
}
