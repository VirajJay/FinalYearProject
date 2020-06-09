from tkinter import *
from tkinter.font import Font

import os;
import serial;
import string;
import time;
from multiprocessing import Process, current_process, Pool, Value

########################################################################
#INITIALISING MFCS
# MFCS class
from Fluigent.MFCS import MFCS

# Get the serial numbers of the available instruments
instrument_serial_numbers = MFCS.detect()

if not instrument_serial_numbers:
    raise Exception("No MFCS Series device detected")
    
print("Available devices: {}". format(instrument_serial_numbers))
########################################################################

global lol;
lol=0;

def ledToggle():
	global lol;
	lol=lol+1;
	print("Button Pressed");

def write_pressure(mfcs_sub1, chnl1, chnl2, chnl3, chnl4):
	chnl1=int(chnl1);
	chnl2=int(chnl2);
	chnl3=int(chnl3);
	chnl4=int(chnl4);
	
	mfcs_sub1[1].set_pressure(chnl1);
	mfcs_sub1[2].set_pressure(chnl2);
	mfcs_sub1[3].set_pressure(chnl3);
	mfcs_sub1[4].set_pressure(chnl4);
	
	print('changed\n');

def gui_func():	
	# Initialize the first instrument in the list
	mfcs = MFCS(instrument_serial_numbers[0]);

	# "print" the initialized device to view its basic information
	print(mfcs);
	
	global lol;
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
	
	#channel pressures in mbar
	channel1_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel1_pressure_disp.grid(row=1, column=0);
	
	channel2_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel2_pressure_disp.grid(row=1, column=1);
	
	channel3_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel3_pressure_disp.grid(row=1, column=2);
	
	channel4_pressure_disp=Label(win, text='0', font=myFont, height=1, width=25);
	channel4_pressure_disp.grid(row=1, column=3);
	
	#channel pressure inputs
	channel1_input=Entry(win);
	channel1_input.grid(row=2, column=0);
	
	channel2_input=Entry(win);
	channel2_input.grid(row=2, column=1);
	
	channel3_input=Entry(win);
	channel3_input.grid(row=2, column=2);
	
	channel4_input=Entry(win);
	channel4_input.grid(row=2, column=3);
	
	#channel pressure request button
	submit=Button(win, text='Request Pressure', font=myFont, height=1, width=25, command=lambda: write_pressure(mfcs, channel1_input.get(), channel2_input.get(), channel3_input.get(), channel4_input.get()));
	submit.grid(row=3, column=0);
	
	while(1):
		#get data from fluigent and configure it as follows:
		channel1_pressure_disp.config(text=round(mfcs.get_pressure(1), 3));
		channel2_pressure_disp.config(text=round(mfcs.get_pressure(2), 3));
		channel3_pressure_disp.config(text=round(mfcs.get_pressure(3), 3));
		channel4_pressure_disp.config(text=round(mfcs.get_pressure(4), 3));
		win.update();
		time.sleep(0.05);
	

if __name__=="__main__":
	gui_proc=Process(target=gui_func);
	gui_proc.start();
	print('LOL');




