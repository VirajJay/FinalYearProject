from tkinter import *
from tkinter.font import Font

import os;
import serial;
import string;
import time;
from multiprocessing import Process, current_process, Pool, Value

global lol;
lol=0;

def ledToggle(txt):
	print(txt);

def gui_func():	
	global lol;
	win=Tk()
	win.title("Test GUI");
	myFont=Font(family='Times New Roman', size=12, weight="bold");
	
	channel1_input=Entry(win);
	channel1_input.grid(row=0, column=1);
	
	ledButton=Button(win, text="Turn LED on", font=myFont, command=lambda: ledToggle(channel1_input.get()), bg='bisque2', height=1, width=25);
	ledButton.grid(row=0, column=2);
	
	while(1):
		win.update();
		time.sleep(0.05);
	

if __name__=="__main__":
	gui_proc=Process(target=gui_func);
	gui_proc.start();
	print('LOL');




