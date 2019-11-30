#coding:utf-8
#从结果反查resp日志

import commands
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import Counter
import math


def loadSuffix():
	fi = open('domainsuffix.txt','r')
	DomainSuffix = []
	for f in fi:
		DomainSuffix.append(f[:-1])
	fi.close()
	print "Suffix Loaded for Detecting.."
	return DomainSuffix

DomainSuffix = loadSuffix()

def mainLabel(domain,DomainSuffix):
	PointSplitResult = domain.split('.')
	if domain.count('.') == 0:
		return domain
	res1 = '.' + PointSplitResult[-1]
	res2 = '.' + PointSplitResult[-2]
	if domain.count('.') == 1:
		return PointSplitResult[0]
	if (res2 in DomainSuffix):
		return PointSplitResult[-3]
	return PointSplitResult[-2]

def loadAlexa():
	fi = open('alexa.txt','r')
	Alexa = []
	for f in fi:
		domain = f[:-1]
		label = mainLabel(domain,DomainSuffix)
		Alexa.append(label)
	print 'Alexa loaded for Detecting'
	return Alexa

Alexa = loadAlexa()

def filter10k(domains):
	rd = []
	for d in domains:
		label = mainLabel(d[:-1],DomainSuffix)
		if label in Alexa:
			continue
		rd.append(d)
	return rd

def findip(filename,ip):
	c = 'grep ' + ip + ' ' + filename
	#print c
	result = commands.getoutput(c)
	return result

def finddomains(result):
	log = result.split('\n')
	dresult = []
	for l in log:
		if l == '':
			continue
		parts = l.split('\t')
		parts = [parts[0],parts[2],parts[8],parts[-3]]
		dresult.append(parts)
	res = pd.DataFrame(dresult).drop_duplicates(3)
	res.columns = ['time','srcip','rcode','domain']
	return res


def feature(domains):
	features = []
	for fulldomain in domains:
		domain = mainLabel(fulldomain,DomainSuffix)
		length = len(domain)
		f_len = float(len(domain))
		count = Counter(i for i in domain).most_common()
		entropy = -sum(j/f_len*(math.log(j/f_len)) for i,j in count)
		#lambda
		count = 0
		for x in domain:
			if x.isdigit():
				count += 1
		numratio = float(count) / float(length)

		count = 0
		for x in domain:
			if x.isalpha():
				count += 1
		alpharatio = float(count) / float(length)

		count = 0
		for x in domain:
			if not(x.isalpha() or x.isdigit() or x == '.'):
				count += 1

		specratio = float(count) / float(length)
		features.append([length,entropy,numratio,alpharatio,specratio])
	return np.array(features)

def cluster(features):
	clusternum = len(features) / 30 + 1
	kmeans = KMeans(n_clusters = clusternum)
	kmeans.fit(features)
	labels = kmeans.labels_
	return labels


def filtertime(detail):
	nxs = detail[detail.nxdga == 1]
	starttime = nxs.time[nxs.head(1).index[0]]
	endtime = nxs.time[nxs.tail(1).index[0]]
	detail = detail[(detail.newtime <= endtime) & (detail.newtime >= starttime)]
	ccs = detail[detail.rcode != '3']
	return ccs


if __name__ == '__main__':
	# filename = 'result/dga_20170519_08_site40.log'
	# respname = '/data/dnslog-sjtu-7days/data2/resp_20170519_08_site40.log'
	pd.set_option('display.max_columns', None)
	pd.set_option('display.max_rows', None)
	pd.set_option('display.width',1000)
	filename = 'dga_20170519_08_site40.log'
	respname = 'resp_20170519_08_site40.log'
	fi = open(filename)
	fw = open('result.txt','w')
	domains = []
	ips = []
	for f in fi:
		if f == '--------\n':
			print ip,domains

			result = findip(respname,ip)
			data = finddomains(result)
			rds = data.domain.values
			features = feature(rds)
			#print features
			labels = pd.Series(cluster(features),index = rds)
			#print labels
			target = []
			#target 为目标标签list
			for d in domains:
				target.append(labels[d+'.'])
			target = pd.Series(target).unique()
			#print target
			alldomains = []
			for t in target:
				alldomains += list(labels[labels == t].index)
			alldomains = filter10k(alldomains)
			#print alldomains
			detail = data[data.domain == alldomains[0]]
			for i in range(1,len(alldomains)):
				detail = detail.append(data[data.domain == alldomains[i]])
			detail = detail.sort_index()
			detail.insert(4,'nxdga',detail.domain.map(lambda x: 1 if x[:-1] in domains else 0))
			detail.insert(1,'newtime',pd.to_datetime(detail.time,format='%Y-%m-%d %H:%M:%S'))
			ccs = filtertime(detail)
			print ccs
			fw.writelines(str(ccs))
			fw.writelines('--------------\n')
			domains = []
			continue
			#break
		#收集同ip下数据
		line = f.strip().split('\t')
		ip = line[0]
		domains.append(line[1])
	fw.close()


		



