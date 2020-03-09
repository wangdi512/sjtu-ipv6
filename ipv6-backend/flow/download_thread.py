import requests
from bs4 import BeautifulSoup 
from tqdm import tqdm
import threading
from Queue import Queue



class myThread(threading.Thread):
      def __init__(self, threadID, urls_queue):
         threading.Thread.__init__(self)
         self.threadID = threadID
         self.urls_queue = urls_queue
                                           
      def run(self):
           while True:
               name = self.urls_queue.get()  
               data = down(name)          
               if data:   
                   print('success')
                   self.urls_queue.task_done()                                                                                                                                                                   
                                                                          
def down(name):
	print(name)
	url = "https://archive.org/download/dnmarchives/"+name
	r = requests.get(url, stream=True,proxies = proxies)
	f = open(name, "wb")
	for chunk in tqdm(r.iter_content(chunk_size=1024)):
    		if chunk:
        		f.write(chunk)
        		f.flush()
	return True



lock = threading.Lock()
urls_queue = Queue()     
proxies = {'http': 'http://127.0.0.1:8118', 'https': 'http://127.0.0.1:8118'}
s = requests.Session()
r = s.get("https://archive.org/download/dnmarchives", proxies = proxies)
soup = BeautifulSoup(r.text,"html5lib")
a = soup.select('table.directory-listing-table > tbody > tr ')
for i , j in enumerate(a):
	if i > 0 :
		name = j.select("td > a")[0].attrs['href']
		urls_queue.put(name)
for i  in range(30):                    
      t = myThread(i,urls_queue) 
      t.setDaemon(True)            
      t.start()
urls_queue.join()
with lock:
      print('down')

