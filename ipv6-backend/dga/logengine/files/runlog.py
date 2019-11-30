# encoding:utf-8
import sys
import logging
import time
 
def writeLog(message):
    logger=logging.getLogger()
    #filename = time.strftime('%Y-%m-%d',time.localtime(time.time()))
 
    handler=logging.FileHandler("/root/logengine/runlog/runlog.txt")
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    logger.info(message)
