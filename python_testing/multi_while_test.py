from multiprocessing import Process, log_to_stderr, get_logger
import logging
import time;

def proc_1():
		print('LOL\n');
		
def proc_2():
		print('LMAO\n');
		
if __name__=='__main__':
	log_to_stderr();
	logger=get_logger();
	logger.setLevel(logging.INFO);
	p1=Process(target=proc_1);
	p2=Process(target=proc_2);
	p1.start();
	p2.start();
	p1.join();
	p1.terminate();
	p2.join();
	p2.terminate();
	time.sleep(2);
	p1.start();
