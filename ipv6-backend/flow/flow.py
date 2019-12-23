import pandas as pd
import os
import threading
from queue import Queue
from multiprocessing import cpu_count
from  flow_thread import myThread
import time

if __name__ == '__main__':
	start = time.clock()
	cpu_count()
	dframe = pd.read_csv("1.flow",sep='\s+')
	dframe=dframe.dropna(axis=0, how='any')
	dframe=dframe.reset_index(drop=True)
	lenth = len(dframe)
	count = int((lenth/cpu_count()))+1
	input_queue = Queue()
	for n in range(cpu_count()):
                if n != cpu_count()-1:
                        input_queue.put([n*count,(n+1)*count])
                else:
                        input_queue.put([n*count,lenth])
	lock = threading.Lock()                                                                                                         
	for i in range(4):                                                                                                 
		t = myThread(i,input_queue,dframe)                                                                            
		t.setDaemon(True)                                                                                               
		t.start()
		#t.join()        
	input_queue.join()                                                                                                   
	#out_queue.join()                                                                                                    
	with lock:                                                                                                          
		print('down')
		print(time.clock()-start)  
