import threading
from queue import Queue
from multiprocessing import cpu_count
from flow_pro import Process

class myThread(threading.Thread):
      def __init__(self, threadID, input_queue,dataframe):
         threading.Thread.__init__(self)
         self.threadID = threadID
         self.input_queue = input_queue
         self.dataframe = dataframe

      def run(self):
           while True:
               n = self.input_queue.get()
               print(self.threadID,n)
               self.input_queue.task_done()
               a = Process(((self.dataframe[n[0]:n[1]]).copy()).reset_index())
               a.test()


