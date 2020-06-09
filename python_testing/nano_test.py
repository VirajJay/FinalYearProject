import serial;
import string;
import time;
import keyboard;

ser=serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=10);

while(1):
	try:
		ser.write('500\n');
		time.sleep(5);
		ser.flush();
	except KeyboardInterrupt:
		ser.flush();
		ser.close();
	except:
		print('ERROR');
	
	
	
