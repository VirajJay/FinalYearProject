import RPi.GPIO as GPIO
import time

trg_1=21;
pwr_1=26;

GPIO.cleanup();
GPIO.setmode(GPIO.BCM);
GPIO.setup(trg_1, GPIO.OUT);
GPIO.setup(pwr_1, GPIO.OUT);
GPIO.setup(19, GPIO.OUT);
GPIO.setup(13, GPIO.OUT);
GPIO.setup(6, GPIO.OUT);
GPIO.setup(5, GPIO.OUT);

GPIO.output(pwr_1, GPIO.HIGH);
GPIO.output(trg_1, GPIO.HIGH);
while(1):
	try:
		"""
		#turn on actuator
		GPIO.output(pwr_1, GPIO.LOW);
		#trigger
		GPIO.output(trg_1, GPIO.LOW);
		GPIO.output(trg_1, GPIO.HIGH);
		#keep valve turned on for 2 seconds
		time.sleep(2);
		#turn off valve
		GPIO.output(pwr_1, GPIO.HIGH);
		#keep valve turned off for 1 second
		time.sleep(1);
		"""
		GPIO.output(pwr_1, GPIO.LOW);
		GPIO.output(pwr_1, GPIO.HIGH);
		GPIO.output(pwr_1, GPIO.LOW);
		"""
		GPIO.output(19, GPIO.LOW);
		GPIO.output(13, GPIO.LOW);
		GPIO.output(6, GPIO.HIGH);
		GPIO.output(5, GPIO.HIGH);
		"""
		print("OFF");
		time.sleep(10);
		
		GPIO.output(pwr_1, GPIO.HIGH);
		"""
		GPIO.output(19, GPIO.HIGH);
		GPIO.output(13, GPIO.HIGH);
		GPIO.output(6, GPIO.LOW);
		GPIO.output(5, GPIO.LOW);
		"""
		print("ON");
		time.sleep(10);
	except KeyboardInterrupt:
		GPIO.cleanup();
		print('done');
		break;
