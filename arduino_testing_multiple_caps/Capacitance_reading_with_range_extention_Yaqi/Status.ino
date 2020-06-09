void displayStatus(char mesg[16]) {
  unsigned char data[18];
  
  readRegisters(0,18,data);
   
  Serial.print("\nAD7746 Registers @: ");
  Serial.println(mesg);
  //Status: 8bits
  Serial.print("Status (0x0): ");
  Serial.print(data[0],HEX);
  Serial.print("h:");
  Serial.println(data[0],BIN);
  //Cap data:  3 bytes
  Serial.print("Cap Data (0x1-0x3): ");
  Serial.print(data[1],BIN);
  Serial.print(".");
  Serial.print(data[2],BIN);
  Serial.print(".");
  Serial.println(data[3],BIN);
  //VT data: 3bytes
  Serial.print("VT Data (0x4-0x6): ");
  Serial.print(data[4],BIN);
  Serial.print(".");
  Serial.print(data[5],BIN);
  Serial.print(".");
  Serial.println(data[6],BIN);
  //Cap Setup 8 bits
  Serial.print("Cap Setup (0x7): ");
  Serial.println(data[7],BIN);
  //VT setup 8bits
  Serial.print("VT Setup (0x8): ");
  Serial.println(data[8],BIN);
  //EXC setup 8bits
  Serial.print("EXC Setup (0x9): ");
  Serial.println(data[9],BIN);
  //Configuration 8bits
  Serial.print("Configuration (0xa): ");
  Serial.println(data[10],BIN);
  //Cap Dac A 8bits
  Serial.print("Cap Dac A (0xb): ");
  Serial.println(data[11],BIN);
  //Cap Dac B 8bits
  Serial.print("Cap Dac B (0xc): ");
  Serial.println(data[12],BIN);
  //Cap offset 2 bytes
  Serial.print("Cap Offset (0xd-0xe): ");
  Serial.print(data[13],BIN);
  Serial.print(".");
  Serial.println(data[14],BIN);
  //Cap Gain 2bytes
  Serial.print("Cap Gain (0xf-0x10): ");
  Serial.print(data[15],BIN);
  Serial.print(".");
  Serial.println(data[16],BIN);
  //Volt Gain 2 bytes
  Serial.print("Volt Gain (0x11-0x12): ");
  Serial.print(data[17],BIN);
  Serial.print(".");
  Serial.println(data[18],BIN);
  
}
