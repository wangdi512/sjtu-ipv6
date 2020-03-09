#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import sys
import runlog

from multiprocessing import Process


class Paths:

    capture = "/root/logengine/pcapfile"
    schedule = capture+"/"+sys.argv[1]+".txt" 
#/home/traffic/pcapfile/bro.txt /home/traffic/pcapfile/pdns_all2.txt /home/traffic/pcapfile/argus.txt


def extract(path):
    print("process %s" % path)
    comname=sys.argv[1]
    print(comname)
    if comname=="bro":
       execmd=comname+" -r "+path+" "+"/home/bro/scripts/plugins/extract-pe.bro"
    elif comname=="pdns":
       execmd=comname+" -i "+path
    elif comname=="pdns_resp":
       execmd=comname+" -i "+path
    elif comname=="pdns_all2":
       execmd=comname+" -i "+path
    elif comname=="pdns3new":
       execmd=comname+" -i "+path
       print(execmd)
    elif comname=="argus":
       filename=path.split("/")[-1]+".flow"
       execmd=comname+" -r "+path+" -w -|ra -r - -s stime dur proto saddr dir daddr sport dport bytes pkts > "+filename
    else:
       print "invalid command"
       exit(1)
    runlog.writeLog("processing:"+execmd)
    os.system(execmd)
    runlog.writeLog("finished:"+execmd)
# bro -r path /home/bro/scripts/plugins/extract-pe.bro
# pdns_all2 -i path
# pdns3new -i path
# argus -r ../2018_1120_0514_2x9.pcap -w -|ra -r - -s stime dur proto saddr dir daddr sport dport bytes pkts > p.flow


def init():
    if not os.path.exists(Paths.schedule):
        with open(Paths.schedule, "wb") as fp:
            pass


def main():
    if len(sys.argv) <> 3:
        print("Usage: python run.py comname(bro|pdns_all2|pdns3new|argus) processes(1-10)")
        exit()
    init()
    finished = []
    with open(Paths.schedule, "rb") as fp:
        for line in fp:
            finished.append(line.strip())
    while True:
        pcaps = []
        for i in os.listdir(Paths.capture):
            if i.endswith(".pcap"):
                pcaps.append(i)
        pcaps.sort()
        #pcaps.pop()
        todo = []
        for p in pcaps:
            if p in finished:
                # print("skip %s" % p)
                continue
            todo.append(p)
            if len(todo) == int(sys.argv[2]):# 5 is ok 
                break
        processes = [
            Process(
                target=extract,
                args=(os.path.join(Paths.capture, p), )
            )
            for p in todo
        ]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        for p in todo:
            finished.append(p)
            with open(Paths.schedule, "ab") as fp:
                fp.write(p + "\n")
        time.sleep(10)


if __name__ == '__main__':
    main()
