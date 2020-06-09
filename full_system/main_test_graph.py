#############################################
#Programmed by Viraj Jayasinghe
#This program is compatible in Python3
#so use command like 'sudo python3 main.py'
#############################################

import os;
import serial;
import string;
import time;
from multiprocessing import Process, current_process, Pool, Value, Lock, Array, Manager

#GUI stuff
from tkinter import *
from tkinter.font import Font
#GUI graphing stuff
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

#GPIO stuff
import RPi.GPIO as GPIO
########################################################################
#INITIALISING MFCS
# MFCS class
from Fluigent.MFCS import MFCS

"""
# Get the serial numbers of the available instruments
instrument_serial_numbers = MFCS.detect()

if not instrument_serial_numbers:
    raise Exception("No MFCS Series device detected")
    
print("Available devices: {}". format(instrument_serial_numbers))
"""
########################################################################

#declare all Value and global variables here:
cap_count=4;

try:
	ser_cap=serial.Serial('/dev/ttyACM0', baudrate=19200, timeout=100);
except:
	print('Could not connect to Capacitive Sensor\n');
	exit(1);

#initialising GPIO for valve actuation

trg_1=37;
pwr_1=5;
trg_2=37;
pwr_2=6;
trg_3=37;
pwr_3=13;
trg_4=37;
pwr_4=19;
trg_5=37;
pwr_5=26;

GPIO.setmode(GPIO.BCM);

GPIO.setup(trg_1, GPIO.OUT);	
GPIO.setup(pwr_1, GPIO.OUT);
GPIO.setup(trg_2, GPIO.OUT);	
GPIO.setup(pwr_2, GPIO.OUT);
GPIO.setup(trg_3, GPIO.OUT);	
GPIO.setup(pwr_3, GPIO.OUT);
GPIO.setup(trg_4, GPIO.OUT);	
GPIO.setup(pwr_4, GPIO.OUT);
GPIO.setup(trg_5, GPIO.OUT);	
GPIO.setup(pwr_5, GPIO.OUT);
	
GPIO.output(pwr_1, GPIO.HIGH);
GPIO.output(pwr_2, GPIO.HIGH);
GPIO.output(pwr_2, GPIO.HIGH);
GPIO.output(pwr_2, GPIO.HIGH);
GPIO.output(pwr_2, GPIO.HIGH);

def stop_program(STOP_PROGRAM):
	GPIO.cleanup();
	STOP_PROGRAM.value=1;

def write_pressure(mfcs_sub1, chnl1, chnl2, chnl3, chnl4, chnl5, chnl6, chnl7, chnl8):
	
	chnl1=int(chnl1);
	chnl2=int(chnl2);
	chnl3=int(chnl3);
	chnl4=int(chnl4);
	chnl5=int(chnl5);
	chnl6=int(chnl6);
	chnl7=int(chnl7);
	chnl8=int(chnl8);

	mfcs_sub1[1].set_pressure(chnl1);
	mfcs_sub1[2].set_pressure(chnl2);
	mfcs_sub1[3].set_pressure(chnl3);
	mfcs_sub1[4].set_pressure(chnl4);
	if(chnl5!="" and chnl6!="" and chnl7!="" and chnl8!=""):
		mfcs_sub1[5].set_pressure(chnl5);
		mfcs_sub1[6].set_pressure(chnl6);
		mfcs_sub1[7].set_pressure(chnl7);
		mfcs_sub1[8].set_pressure(chnl8);
	
	print('Pressure levels changed\n');
	
def cap_sensor(source, STOP_PROGRAM, cap_vals, keep_saving):
	time_init=time.time();
	new_data=[0]*(cap_count+1);
	while 1:
		if(STOP_PROGRAM.value==1):
			source.close();
			print('cap_sensing stopped');
			sys.exit();
		try:
			data=source.readline();
			data=data.decode('utf-8');
			#print(repr(data));
			data=data.split("\t");
			data[-1]=data[-1].replace("\r\n", "")
			new_data[0]=time.time()-time_init;
			for i in range(len(data)):
					new_data[i+1]=int(data[i]);
			cap_vals.append(new_data);
			if(len(cap_vals)>10000):#to save memory
				if(keep_saving.value==0):
					print('some data deleted to save memory');
					del(cap_vals[0:9999]);
		except KeyboardInterrupt:
			source.close();
			break;
		except Exception as e:
			print("cap_sense error: "+str(e));

def valve_test():
	#turn on the valve
	GPIO.output(valve_power, GPIO.HIGH);
	#time.sleep(0.025);
	time.sleep(1);
	GPIO.output(valve_SPDT, GPIO.HIGH);
	time.sleep(2.5);
	GPIO.output(valve_power, GPIO.LOW);
	time.sleep(0.025);
	GPIO.output(valve_SPDT, GPIO.LOW);
	
def change_cap_thresold(cap_threshold, new_cap_threshold, min_val, max_val, min_pressure_val, max_pressure_val):
	cap_threshold.value=int(new_cap_threshold);
	try:
		min_pressure_val.value=int(min_val);
		max_pressure_val.value=int(max_val);
	except Exception as e:
		print("threshold change error: "+str(e));
	print('Capacitor threshold updated');

def fluigent(STOP_PROGRAM, cap_threshold, cap_vals, min_pressure_val, max_pressure_val, VALVE_ACT, keep_saving):
	
	# Initialize the first instrument in the list
	#mfcs = MFCS(instrument_serial_numbers[0]);

	# "print" the initialized device to view its basic information
	#print(mfcs);

	win=Tk()
	win.title("Test GUI");
	myFont=Font(family='Times New Roman', size=12, weight="bold");
	
	
	#ledButton=Button(win, text="Turn LED on", font=myFont, command=ledToggle, bg='bisque2', height=1, width=25);
	#ledButton.grid(row=0, column=1);
	
	#Channel Labels
	channel1_pressure_label=Label(win, text='Channel One Pressure: ', font=myFont, height=1, width=25);
	channel1_pressure_label.grid(row=0, column=0);
	
	channel2_pressure_label=Label(win, text='Channel Two Pressure: ', font=myFont, height=1, width=25);
	channel2_pressure_label.grid(row=0, column=1);
	
	channel3_pressure_label=Label(win, text='Channel Three Pressure: ', font=myFont, height=1, width=25);
	channel3_pressure_label.grid(row=0, column=2);
	
	channel4_pressure_label=Label(win, text='Channel Four Pressure: ', font=myFont, height=1, width=25);
	channel4_pressure_label.grid(row=0, column=3);
	
	channel5_pressure_label=Label(win, text='Channel Five Pressure: ', font=myFont, height=1, width=25);
	channel5_pressure_label.grid(row=3, column=0);
	
	channel6_pressure_label=Label(win, text='Channel Six Pressure: ', font=myFont, height=1, width=25);
	channel6_pressure_label.grid(row=3, column=1);
	
	channel7_pressure_label=Label(win, text='Channel Seven Pressure: ', font=myFont, height=1, width=25);
	channel7_pressure_label.grid(row=3, column=2);
	
	channel8_pressure_label=Label(win, text='Channel Eight Pressure: ', font=myFont, height=1, width=25);
	channel8_pressure_label.grid(row=3, column=3);
	
	#channel pressures in mbar
	channel1_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel1_pressure_disp.grid(row=1, column=0);
	
	channel2_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel2_pressure_disp.grid(row=1, column=1);
	
	channel3_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel3_pressure_disp.grid(row=1, column=2);
	
	channel4_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel4_pressure_disp.grid(row=1, column=3);
	
	channel5_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel5_pressure_disp.grid(row=4, column=0);
	
	channel6_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel6_pressure_disp.grid(row=4, column=1);
	
	channel7_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel7_pressure_disp.grid(row=4, column=2);

	channel8_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel8_pressure_disp.grid(row=4, column=3);
	
	#channel pressure inputs
	channel1_input=Entry(win);
	channel1_input.grid(row=2, column=0);
	
	channel2_input=Entry(win);
	channel2_input.grid(row=2, column=1);
	
	channel3_input=Entry(win);
	channel3_input.grid(row=2, column=2);
	
	channel4_input=Entry(win);
	channel4_input.grid(row=2, column=3);
	
	channel5_input=Entry(win);
	channel5_input.grid(row=5, column=0);
	
	channel6_input=Entry(win);
	channel6_input.grid(row=5, column=1);
	
	channel7_input=Entry(win);
	channel7_input.grid(row=5, column=2);
	
	channel8_input=Entry(win);
	channel8_input.grid(row=5, column=3);
	
	#channel pressure request button
	"""
	submit=Button(win, text='Request Pressure', font=myFont, height=1, width=25, command=lambda: write_pressure(mfcs, channel1_input.get(), channel2_input.get(), channel3_input.get(), channel4_input.get(), channel5_input.get(), channel6_input.get(), channel7_input.get(), channel8_input.get()));
	submit.grid(row=8, column=0);
	"""
	
	#capacitor output displays
	cap_one_text=Label(win, text='Capacitor One: ', font=myFont, height=1, width=25);
	cap_one_val=Label(win, text=str(cap_vals[-1][1]), font=myFont, height=1, width=25);
	cap_one_text.grid(row=6, column=0);
	cap_one_val.grid(row=7, column=0);
	
	cap_two_text=Label(win, text='Capacitor Two: ', font=myFont, height=1, width=25);
	cap_two_val=Label(win, text=str(cap_vals[-1][2]), font=myFont, height=1, width=25);
	cap_two_text.grid(row=6, column=1);
	cap_two_val.grid(row=7, column=1);
	
	cap_three_text=Label(win, text='Capacitor Three: ', font=myFont, height=1, width=25);
	cap_three_val=Label(win, text=str(cap_vals[-1][3]), font=myFont, height=1, width=25);
	cap_three_text.grid(row=6, column=2);
	cap_three_val.grid(row=7, column=2);
	
	cap_four_text=Label(win, text='Capacitor Four: ', font=myFont, height=1, width=25);
	cap_four_val=Label(win, text=str(cap_vals[-1][4]), font=myFont, height=1, width=25);
	cap_four_text.grid(row=6, column=3);
	cap_four_val.grid(row=7, column=3);
	
	save_file_path=Entry(win);
	save_file_path.grid(row=10, column=0);
	
	def toggle_data_save(keep_saving):
		global cap_count;
		start_point=0;
		finish_point=0;
		if(keep_saving.value==1):
			finish_point=len(cap_vals)-1;
			print('writing data to file......');
			save_str='Time\t\tCap_one\t\tCap_two\t\tCap_three\t\tCap_four\n';
			for i in range(start_point, finish_point):
				save_str+="{:10.4f}\t".format(cap_vals[i][0]-cap_vals[start_point][0]);#save the time value
				for j in range(cap_count):#save capacitor values
					save_str+="\t{}\t".format(cap_vals[i][j+1]);
				save_str+="\n";				
			f=open(save_file_path.get(), "+a");
			f.write(save_str);
			f.close();	
			print('finished writing data to file......');	
			keep_saving.value=0;
		else:
			keep_saving.value=1;
			start_point=len(cap_vals)-1;
			print('save point stored.....');	
			#this function sends command to the computer to start recording
			ser_1=serial.Serial('/dev/ttyS0', baudrate=115200, timeout=10);
			ser_1.flush();
			count_send=0;
			while(count_send<3):
				ser_1.write(str.encode('1'));
				count_send+=1;
			ser_1.close();	
	
	btn_save_data=Button(win, text='Save Data', font=myFont, height=1, width=25, command=lambda: toggle_data_save(keep_saving));
	btn_save_data.grid(row=11, column=0);
	
	#valve testing button
	btn_valve_test=Button(win, text='Test Valves', font=myFont, height=1, width=25, command=valve_test);
	btn_valve_test.grid(row=11, column=3);
	
	#terminate program button
	btn_terminate=Button(win, text='STOP PROGRAM', font=myFont, height=1, width=14, bg='red', command=lambda: stop_program(STOP_PROGRAM));
	btn_terminate.grid(row=4, column=4);
	
	min_pressure=Entry();
	max_pressure=Entry();
	lbl_min_pressure=Label(win, text='low-end: ', font=myFont, height=1, width=25);
	lbl_max_pressure=Label(win, text='high-end: ', font=myFont, height=1, width=25);
	lbl_min_pressure.grid(row=8, column=2);
	lbl_max_pressure.grid(row=8, column=3);
	min_pressure.grid(row=9, column=2);
	max_pressure.grid(row=9, column=3);
	cap_threshold_input=Entry();
	btn_new_threshold=Button(win, text='New Threshold', font=myFont, height=1, width=25, command=lambda: change_cap_thresold(cap_threshold, cap_threshold_input.get(), min_pressure.get(), max_pressure.get(), min_pressure_val, max_pressure_val));
	cap_threshold_input.grid(row=9, column=4);
	btn_new_threshold.grid(row=10, column=4);

	def change_program_mode():
		if(btn_toggle_mode["text"]=="Manual Mode"):
			submit.config(state=DISABLED);
			btn_new_threshold.config(state='normal');
			btn_toggle_mode.config(text="Loading Mode")
		elif(btn_toggle_mode["text"]=="Loading Mode"):
			submit.config(state='normal');
			btn_new_threshold.config(state=DISABLED);
			btn_toggle_mode.config(text="Manual Mode")

	btn_toggle_mode=Button(win, text='Loading Mode', font=myFont, height=1, width=25, command=change_program_mode);
	btn_toggle_mode.grid(row=11, column=1);
	
	lbl_chamber_valve=Label(win, text='Chamber Valve', font=myFont, height=1, width=25, bg='grey');
	lbl_chamber_valve.grid(row=12, column=2);
	lbl_outlet_valve=Label(win, text='Outlet Valve', font=myFont, height=1, width=25, bg='grey');
	lbl_outlet_valve.grid(row=12, column=3);
	
	while(1):
		"""
		#get data from fluigent and configure it as follows:
		channel1_pressure_disp.config(text=round(mfcs.get_pressure(1), 3));
		channel2_pressure_disp.config(text=round(mfcs.get_pressure(2), 3));
		channel3_pressure_disp.config(text=round(mfcs.get_pressure(3), 3));
		channel4_pressure_disp.config(text=round(mfcs.get_pressure(4), 3));
		channel5_pressure_disp.config(text=round(mfcs.get_pressure(5), 3));
		channel6_pressure_disp.config(text=round(mfcs.get_pressure(6), 3));
		channel7_pressure_disp.config(text=round(mfcs.get_pressure(7), 3));
		channel8_pressure_disp.config(text=round(mfcs.get_pressure(8), 3));
		"""
		if(VALVE_ACT.value==1):
			if(lbl_chamber_valve["bg"]=='grey'):
				lbl_chamber_valve.config(bg='green');
		else:
			if(lbl_chamber_valve["bg"]=='green'):
				lbl_chamber_valve.config(bg='grey');
			
		#update capacitor display values
		cap_one_val.config(text=str(cap_vals[-1][1]));
		cap_two_val.config(text=str(cap_vals[-1][2]));
		cap_three_val.config(text=str(cap_vals[-1][3]));
		cap_four_val.config(text=str(cap_vals[-1][4]));
		if(keep_saving.value==1):
			btn_save_data.config(text='SAVING DATA');
		else:
			btn_save_data.config(text='Save Data');
		win.update();
		#time.sleep(0.05);
		if(STOP_PROGRAM.value==1):
			print('fluigent stopped');
			sys.exit();		

def loading_mode(STOP_PROGRAM, cap_threshold, cap_vals, min_pressure_val, max_pressure_val, VALVE_ACT):
	while(1):		
		if(STOP_PROGRAM.value==1):
			print('loading mode stopped');
			sys.exit();
			
		else:
			continue
			#do this for each cap
			if(cap_threshold.value>cap_vals[-1][1]):#turn on actuator
				#mfcs_sub1[6].set_pressure(min_pressure_val.value);
				#trigger the 12v for 25ms
				GPIO.output(trg_1, GPIO.LOW);
				GPIO.output(trg_1, GPIO.HIGH);
				#turn on power
				GPIO.output(pwr_1, GPIO.LOW);
				time.sleep(0.1);
			else:#turn off actuator
				#mfcs_sub1[6].set_pressure(max_pressure_val.value);
				#turn on valve
				print('Capacitor 1 threshold reached');
				print(cap_threshold.value);
				GPIO.output(pwr_1, GPIO.HIGH);
				time.sleep(0.1);
			if(cap_threshold.value>cap_vals[-1][2]):#turn on actuator
				#mfcs_sub1[6].set_pressure(min_pressure_val.value);
				#trigger the 12v for 25ms
				GPIO.output(trg_2, GPIO.LOW);
				GPIO.output(trg_2, GPIO.HIGH);
				#turn on power
				GPIO.output(pwr_2, GPIO.LOW);
				time.sleep(0.1);
			else:#turn off actuator
				#mfcs_sub1[6].set_pressure(max_pressure_val.value);
				#turn on valve
				print('Capacitor 2 threshold reached');
				GPIO.output(pwr_2, GPIO.HIGH);
				time.sleep(0.1);
			if(cap_threshold.value>cap_vals[-1][3]):#turn on actuator
				#mfcs_sub1[6].set_pressure(min_pressure_val.value);
				#trigger the 12v for 25ms
				GPIO.output(trg_3, GPIO.LOW);
				GPIO.output(trg_3, GPIO.HIGH);
				#turn on power
				GPIO.output(pwr_3, GPIO.LOW);
				time.sleep(0.1);
			else:#turn off actuator
				#mfcs_sub1[6].set_pressure(max_pressure_val.value);
				#turn on valve
				print('Capacitor 3 threshold reached');
				GPIO.output(pwr_3, GPIO.HIGH);
				time.sleep(0.1);
			if(cap_threshold.value>cap_vals[-1][4]):#turn on actuator
				#mfcs_sub1[6].set_pressure(min_pressure_val.value);
				#trigger the 12v for 25ms
				GPIO.output(trg_4, GPIO.LOW);
				GPIO.output(trg_4, GPIO.HIGH);
				#turn on power
				GPIO.output(pwr_4, GPIO.LOW);
				time.sleep(0.1);
			else:#turn off actuator
				#mfcs_sub1[6].set_pressure(max_pressure_val.value);
				#turn on valve
				print('Capacitor 4 threshold reached');
				GPIO.output(pwr_4, GPIO.HIGH);
				time.sleep(0.1);
				
def plot_graph(STOP_PROGRAM, cap_vals):
	ax=plt.subplot(2, 2, 1);
	ax_2=plt.subplot(2, 2, 2);
	ax_3=plt.subplot(2, 2, 3);
	ax_4=plt.subplot(2, 2, 4);
	ax.title.set_text('Cap_1');
	ax_2.title.set_text('Cap_2');
	ax_3.title.set_text('Cap_3');
	ax_4.title.set_text('Cap_4');
	disp_range=20;
	x_lower=0;
	#plt.axis(xmin=x_lower, xmax=x_lower+disp_range, ymin=0, ymax=2*3380000);
	ax.set_xlim([x_lower, x_lower+disp_range]);
	ax.set_ylim([0, 16777215]);
	ax_2.set_xlim([x_lower, x_lower+disp_range]);
	ax_2.set_ylim([0, 16777215]);
	ax_3.set_xlim([x_lower, x_lower+disp_range]);
	ax_3.set_ylim([0, 16777215]);
	ax_4.set_xlim([x_lower, x_lower+disp_range]);
	ax_4.set_ylim([0, 16777215]);
	data=cap_vals[-1];
	while(1):
		if(STOP_PROGRAM.value==1):
			plt.close();
			print('graphing mode stopped');
			break;
		else:
			if(data[0]!=cap_vals[-1][0]):
				data=cap_vals[-1];
				if(data[0]>x_lower+disp_range):
					x_lower=data[0];
					ax.clear();
					ax_2.clear();
					ax_3.clear();
					ax_4.clear();
					ax.title.set_text('Cap_1');
					ax_2.title.set_text('Cap_2');
					ax_3.title.set_text('Cap_3');
					ax_4.title.set_text('Cap_4');
					ax.set_xlim([x_lower, x_lower+disp_range]);
					ax.set_ylim([0, 16777215]);
					ax_2.set_xlim([x_lower, x_lower+disp_range]);
					ax_2.set_ylim([0, 16777215]);
					ax_3.set_xlim([x_lower, x_lower+disp_range]);
					ax_3.set_ylim([0, 16777215]);
					ax_4.set_xlim([x_lower, x_lower+disp_range]);
					ax_4.set_ylim([0, 16777215]);
					
				ax.plot(data[0], data[1], '-ob');
				ax_2.plot(data[0], data[2], '-ob');
				ax_3.plot(data[0], data[3], '-ob');
				ax_4.plot(data[0], data[4], '-ob');
				plt.pause(0.0001);

if __name__=="__main__":
	keep_saving=Value('i', 0);
	VALVE_ACT=Value('i', 0);
	STOP_PROGRAM=Value('i', 0);
	cap_threshold=Value('i', 0);
	min_pressure_val=Value('i', 0);
	max_pressure_val=Value('i', 10);
	manager=Manager();
	cap_vals=manager.list();
	
	
	#define the processes
	
	cap_sensor_proc=Process(target=cap_sensor, args=(ser_cap, STOP_PROGRAM, cap_vals, keep_saving, ));
	fluigent_proc=Process(target=fluigent, args=(STOP_PROGRAM, cap_threshold, cap_vals, min_pressure_val, max_pressure_val, VALVE_ACT, keep_saving, ));
	loading_mode_proc=Process(target=loading_mode, args=(STOP_PROGRAM, cap_threshold, cap_vals, min_pressure_val, max_pressure_val, VALVE_ACT, ));
	plot_graph_proc=Process(target=plot_graph, args=(STOP_PROGRAM, cap_vals, ));
	
	#run the processes
	print('starting cap_sensor process...');
	cap_sensor_proc.start();
	time.sleep(5);
	print('starting fluigent process...');
	fluigent_proc.start();#gui stuff also runs here
	print('starting loading_mode process...');
	loading_mode_proc.start();
	print('starting plot_graph process...');
	plot_graph_proc.start();
	#print(cap_vals);
	
	#join processes in the end
	cap_sensor_proc.join();
	fluigent_proc.join();
	loading_mode_proc.join();
	plot_graph_proc.join();
	print('Program Exit');
	
