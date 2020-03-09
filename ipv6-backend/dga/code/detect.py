#coding:utf-8
import os
import time

if __name__ == '__main__':
	logpath = '/log/dga'
	p = []
        if os.path.exists('/log/dga/processed.txt'):
		fi = open('/log/dga/processed.txt')
		for f in fi:
			p.append(f[:-1])
	files = os.listdir(logpath)
	files = [os.path.join(logpath,file) for file in files]
	files = [file for file in files if 'dga' in file]
        files = [file for file in files if not os.path.isdir(file)]
	#files = ['/log/dga/dga_20170519_08_site40.log']

	for file in files:
		if file in p:
			continue
		os.system('/opt/spark/dist/bin/spark-submit --master local[*] /deploy/dga/dga3.py '+ file + ' 20')
		fw = open('/log/dga/processed.txt','a')
		fw.writelines(file+'\n')
		fw.close()
	time.sleep(10)	
