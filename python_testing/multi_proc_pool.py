import time
from multiprocessing import Pool

def sum_square(number):
	s=0;
	for i in range(number):
		s+=i*i;
	return s;

if __name__=='__main__':
	numbers=[0, 1, 2, 3, 4];
	p=Pool();
	result=p.map(sum_square, numbers);
	print(result);
	
	p.close();
	p.join();
	
