import os;
from multiprocessing import Process, current_process

def square(num):
	result=num*num;
	
	process_id=os.getpid();
	count=0;
	while(1):
		count=count+1;
		if count>100000000:
			break;
	
	proc_name=current_process().name;
	
	print('The number {} squares to {}. PID: {}. Name: {}'.format(num, result, process_id, proc_name));
	
if __name__=='__main__':
	numbers=[1, 2, 3, 4, 3]
	for number in numbers:
		process=Process(target=square, args=(number,))
		process.start();
