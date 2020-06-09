#include <Wire.h>

//AD7746 definitions
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


void setup()
{
pinMode(18, INPUT);
pinMode(19, INPUT);
 // pinMode(8, OUTPUT);
  //pinMode(7, INPUT);

  Wire.begin(); // sets up i2c for operation
  Serial.begin(19200); // set up baud rate for serial monitor

  Serial.println("\nInitializing_mds-v1");

  //Serial.println(readCapValue());

  Wire.beginTransmission(I2C_ADDRESS); // start i2c cycle
  Wire.write(RESET_ADDRESS); // reset the device
  Wire.endTransmission(); // ends i2c cycle


  //wait a tad for reboot
  delay(1);
  //Serial.println(readValue());

  displayStatus("PreSetup"); //We should have default reset condition.
  
  //Setup CAPDAC Registers
  writeRegister(REGISTER_CAP_SETUP,_BV(7)); // cap setup reg - cap enabled
  writeRegister(REGISTER_VT_SETUP, _BV(7)); //enable Volt/Tempearture reading
  writeRegister(REGISTER_EXC_SETUP, _BV(4) | _BV(3) | _BV(1) | _BV(0)); // EXC A&B on
  //writeRegister(REGISTER_EXC_SETUP, _BV(3)); // EXC A on
  
  //writeRegister(REGISTER_CAP_DAC_A, _BV(7) | 0x40); //CAPDAC+ on, half offset
  
  //Serial.println("Getting offset");
  //offset = ((unsigned long)readInteger(REGISTER_CAP_OFFSET)) << 8;
  //Serial.print("Factory offset: ");
  //Serial.println(offset);
  
  // set configuration to calib. mode, slow sample
  //writeRegister(REGISTER_CONFIGURATION, _BV(7) | _BV(6) | _BV(5) | _BV(4) | _BV(3) | _BV(2) | _BV(0));  

  //wait for calibration
  //delay(1);

  //Serial.print("Calibrated offset: ");
  //offset = ((unsigned long)readInteger(REGISTER_CAP_OFFSET)) << 8;
  //Serial.println(offset);
  
  //writeRegister(REGISTER_CAP_SETUP, _BV(7)); //cin1
  //writeRegister(REGISTER_CAP_SETUP, _BV(7) | _BV(6)); // cin2, cap setup reg - cap enabled

  //writeRegister(REGISTER_EXC_SETUP, _BV(5) | _BV(3)); // EXC source A & B

  // writeRegister(REGISTER_CONFIGURATION, _BV(7) | _BV(6) | _BV(5) | _BV(4) | _BV(3) | _BV(0)); // continuous mode
  //writeRegister(REGISTER_CONFIGURATION, _BV(0)); //continuous, 90Hz, max filter
  
  //try cin2
  //writeRegister(REGISTER_CAP_SETUP, _BV(7) | _BV(6));
  //to calibrate
  //writeRegister(REGISTER_CONFIGURATION, _BV(7) | _BV(6) | _BV(5) | _BV(4) | _BV(3) | _BV(2) | _BV(0));  

  calibrate();

  displayStatus("ChkSetup");
writeRegister(REGISTER_CONFIGURATION, _BV(0)); //continuous, 90Hz, max filter
  //Serial.println("done");
  //Serial.println(millis());

}
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void loop() // main program begins
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
{
  long preval=0; //Stores previous value for filtering purposes
  long capval=0;// stores current cap value
  long vt_val=0;  //stores voltage temp data

  
  capval=readCapValue(); //read cap value from registers
  vt_val=readVtValue(); //read VT value from registers
  //capval=capval-offset;
  //capval=capval/0x1000;
  //if (capval > 0) {
    /*Serial.print(readValue());
    writeRegister(REGISTER_CAP_SETUP, _BV(7) | _BV(6));
    delay(30);
    Serial.print("\t");*/
    Serial.println(capval);  //displays in femtofarads (/1000 for PF)
   // Serial.println(vt_val); //Displays Deg c
    preval=capval;  //save new value
  //}
  delay(100);
}
//~~~~~~~~~~~~~~~~~~~~~~
void calibrate() {
//~~~~~~~~~~~~~~~~~~~~~~
  calibration =32;
  writeRegister(REGISTER_CAP_DAC_A, _BV(7) | calibration);
  delay(10);
//writeRegister(REGISTER_CAP_DAC_B, _BV(7) | calibration);
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
///~~~~~~~~~~~~~~~~~~~~~~~~~~
// Read Voltage Temperature
//~~~~~~~~~~~~~~~~~~~~~~~~~~~
long readVtValue() {
  long ret = 0;
  uint8_t data[3];

  unsigned long value =  readLong(REGISTER_VT_DATA); //Read "4bytes" from Voltage/Temperature register
  //readLong() reads one byte too many, we have to get rid of it
  value >>= 8;

  ret =  value;
  return ret;
}
