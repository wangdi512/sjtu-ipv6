#!/usr/bin/env python
# -*- coding: utf-8 -*-

import schedule
import time
import datetime
import os
import runlog

def exerm():
  #2018_1120_0449_29.pcap
    #os.system("ls -l /home/traffic/pcapfile|grep $(date -d '2 days ago' +%Y_%m_%d)|awk '{print $9}'|xargs rm -f")
        runlog.writeLog("preparing delete file...")
	os.system("find /root/logengine/pcapfile -type f -mtime +1 -name '*.pcap'|grep -E './20[0-9][0-9]_[0-1][0-9]_[0-3][0-9]_'|xargs rm -f")
        runlog.writeLog("finished!")
#设定每天运行的时间
schedule.every().day.at("1:00").do(exerm)

while True:
    schedule.run_pending()
    time.sleep(1)


