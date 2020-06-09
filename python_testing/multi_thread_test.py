import threading
import Queue;
import time;

def test_lol(num1, num2):
	while(1):
		print(num1+num2)
		
def sleep_func(sleep_time, name):
	print('Hi, I am {}. Going to sleep for {} seconds\n'.format(name, sleep_time));
	print(time.localtime());
	time.sleep(sleep_time);
	print(time.localtime());
	print('{} has woken up from sleep \n'.format(name));

if __name__=='__main__':
	t=threading.Thread(target=sleep_func, name='thread 1', args=(5, 'thread 1'))
	u=threading.Thread(target=sleep_func, name='thread 2', args=(10, 'thread 2'))
	t.start();
	print('LOL these guys are sleeping');
	u.start();
	while(1):
		print('LOL')
	time.sleep(40);

