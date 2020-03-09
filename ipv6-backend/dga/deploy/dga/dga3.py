#coding:utf-8
import re
import sys
import os
from math import log
from publicsuffixlist import PublicSuffixList
from pyspark import SparkContext
from operator import add
from sklearn import preprocessing
import numpy
import string
import MySQLdb
import random


filter_file='/deploy/top-1m.txt' # for cluster
filter_file2='/deploy/top-10k.txt' # for init
filter_file3='/deploy/tlds-alpha-by-domain.txt' # for filter dga


MaxVecLen=1000 #1G Mem?

'''
计算两个向量之间的欧几里得距离
'''
def Euclidean_distance(vector1, vector2):
	return sum([(vector1[1][i] - vector2[1][i])**2 for i in range(len(vector1[1]))])

'''
每一个vector对应一个element
'''
class element:
	def __init__(self, vec, left=None, right=None):
		self.vec = vec
		self.left = left # 左叶子节点
		self.right = right # 右叶子节点
'''
搜索出该聚类下的所有叶子节点
'''
def tree_search(elem):
	if elem.left == None and elem.right == None:
		return [elem.vec]
	return tree_search(elem.left) + tree_search(elem.right)

'''
聚类函数
'''
def hcluster(vectors, max_mindist=0.0, min_clusternum=1, func = Euclidean_distance):

	import datetime
	starttime = datetime.datetime.now()

        veclen=len(vectors)
        if veclen>MaxVecLen: vectors=random.sample(vectors,MaxVecLen)
	elements = [ element(vec = vectors[i]) for i in range(len(vectors)) ]
	num_elements = len(elements)
        #print "num_elements:",num_elements
	''' 初始化距离矩阵 '''
	distance_matrix = [[func(
				elements[i].vec, elements[j].vec) 
				for i in range(num_elements)] 
				for j in range(num_elements)]

	flag = None
	while(num_elements > min_clusternum):
		min_distance = float('inf');
		''' 在distance_matrix找出最小距离及所在位置 '''
		for i in range(num_elements-1):
			for j in range(i+1, num_elements):
				if distance_matrix[i][j] < min_distance:
					min_distance = distance_matrix[i][j]
					flag = (i, j)
		if min_distance > max_mindist: break # 如果最小距离超过设定的最大值，结束
		index_elem1, index_elem2 = flag # 赋值于将要聚类的两个element的index
		''' 修改distance_matrix，修改聚类后的距离为两者中较小的那一个值，保存在原来的elem1的位置 '''
		for i in range(num_elements):
			distance_matrix[i][index_elem1] = distance_matrix[index_elem1][i] \
			= (distance_matrix[index_elem1][i]+distance_matrix[index_elem2][i])/2.0
			#distance_matrix[i][index_elem1] = distance_matrix[index_elem1][i] \
			#= min(distance_matrix[index_elem1][i],distance_matrix[index_elem2][i])
			#distance_matrix[i][index_elem1] = distance_matrix[index_elem1][i] \
			#= max(distance_matrix[index_elem1][i],distance_matrix[index_elem2][i])
		''' 删除distance_matrix中原来的elem2的行和列 '''
		for i in range(num_elements):
			del distance_matrix[i][index_elem2]
		del distance_matrix[index_elem2]
		''' 将elem1替换为新的elem，并删除elem2 '''
		new_elem = element(None, left=elements[index_elem1], right=elements[index_elem2])
		elements[index_elem1] = new_elem
		del elements[index_elem2]
		num_elements = len(elements)
	sys.setrecursionlimit(10000)
	clusters = [tree_search(elements[i]) for i in range(len(elements))]

	#long running
	endtime = datetime.datetime.now()
	#print (endtime - starttime).seconds,"seconds"

	return clusters

if __name__ == '__main__':
	c = [('a', [1, 2]),
		 ('a', [3, 4]),
		 ('asd', [100, 100]),
		 ('asdwdq', [80, 2])
	]
	clusters = hcluster(c, 3.0, 4)
	print 'clusters:\n', clusters
	print 'num of clusters:', len(clusters)


def Qlen(QName):
    return len(QName) if QName else 0

def Qtagnum(QName):
    return len(QName.split('.')) if QName else 0

def my_count(string):
    return string.count('.') + 1 if string else 0

def Weight(tmp):
    if len(tmp) == 0:
        return 0
    return round(len(set(tmp)) / float(len(tmp)), 3)

def First(MainDomain):
    ret = []
    tmp = MainDomain.split('.')[0] if MainDomain  else ''
    num = [i for i in tmp if i.isdigit()]
    alp = [i for i in tmp if i.isalpha()]
    ret.append( tmp )
    ret.append( len(tmp) )
    ret.append( Weight(tmp) )
    ret.append( Weight(num) )
    ret.append( Weight(alp) )
    ret.append( tmp.count('-') )
    return ret

def map_r(a, b, func):
    ret = []
    for i, j in zip(a, b):
        ret.append(func(i, j))
    return ret

def m1(l):
    ret = []
    for items, s, l in zip(l, min_l, max_l):
        if s == l:
            ret.append(0)
        else:
            tmp = (items - s) / float(l - s)
            ret.append(round(tmp, 3))
    return ret

def m2(count):
    # zero overflow
    if l_c==s_c: return [0]
    return [round(log(count + 1) / log(l_c - s_c), 3)]

def distance_func(v1, v2):
    return sum([(v1[1][i] - v2[1][i])**2 for i in range(len(v1[1]))])


def loadTable(filter_file):
    dict = {}
    for i in open(filter_file, 'r'):
        dict[i[:-1]] = 1
    return dict

def filter_white(url):
    return filterTable.value.get(string.lower(url), 0)

def filter_white_init(domain):
    if domain==None:return False
    domain=string.lower(domain)
    tld=domain.split('.')[-1]
    return filterTable3.value.get(tld,0)<>0 and filterTable2.value.get(domain, 0)<>1

def filter_input(line):
    if len(line.split("\t")) == 3:
    	return True
    return False

def deal_each_c(cluster):
    count = len(cluster)
    if count == 1:
        return (cluster[0][0][0],filter_white(cluster[0][0][1]), 1, 0, 0, 1)
    else:
        domains,tags, white = [], [], 0
        url_max, url_min = 0, float('inf')
        tag_max, tag_min = 0, float('inf')
        for item in cluster:
            domains.append(item[0][0])
            white += filter_white(item[0][1])
            tags.append(item[0][2])
            url_num = my_count(item[0][0]) + 1
            tag_num = my_count(item[0][1]) + 1
            url_max, url_min = max(url_max, url_num), min(url_min, url_num)
            tag_max, tag_min = max(tag_max, tag_num), min(tag_min, tag_num)
        diff = len(set(tags))
        return (domains,round(float(white) / count, 3), round(float(diff) / count, 3), url_max - url_min, tag_max - tag_min, count)

def filter_result(feature,leastdomains):
    for f in feature:
      if f[5]>leastdomains:
         return True
    return False

# for realtime check
def filter_cluster(p,leastdomains):
    count = len(p)
    ret=[]
    val=0
    for i in p:
      if int(i[5])>=leastdomains and int(i[4])==0 and int(i[3])==0 and float(i[2])>0.90 and float(i[1])<0.05:
	 val+=i[4] 
	 ret.append(i)
    return len(ret),val,ret

# for test normal/dga   
def filter_clusterx(p,leastdomains):
    count = len(p)
    ret=[]
    val=0
    for i in p:
      if int(i[5])>=leastdomains:
          val+=i[4]
	  ret.append((i))
    return len(ret),val,ret

def print_cluster(ip,l,v,p):
    print ip,l,v
    count = len(p)
    for i in p:
     print i

def insert_mysql(p,filename):
  try:
    fw = open('/log/result/' + filename,'a')
    ip=p[0]
    if int(p[1][0])<>0:
      details=p[1][2]
      for dt in details:
        for d in dt[0]:
            fw.writelines(ip + '\t' + d + '\n')
        fw.writelines('--------\n')
      print "logged..."

  except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def f(iterator): 
   yield insert_mysql(iterator)

def f2(rddp):
   for p in rddp:
     insert_mysql(p)
    

if __name__ == "__main__":
    # Initialize the spark context.
    a = sys.argv[1]
    filename = "file://"+a #/home/xky/url-scan/data.log"
    print "filename:",filename
    sc = SparkContext(appName="DGA Detection")
    psl = PublicSuffixList()
    filterTable= sc.broadcast(loadTable(filter_file))
    filterTable2= sc.broadcast(loadTable(filter_file2))
    filterTable3= sc.broadcast(loadTable(filter_file3))
    global conn
    #conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd = "", db ="dns")

    lines = sc.textFile(filename)
  #  lines = lines.filter(filter_white_init) #only a few domains filtered for Alexa 10k. Not here, because we neeed domains as arguments.
    lines = lines.filter(filter_input)
    part = lines.map( lambda p: [p[:-1].split("\t", 1)[1], 1] ).reduceByKey(add) \
                .map( lambda p: p[0].split('\t') + [p[1]] ) \
                .map( lambda p: p + [ psl.privatesuffix(p[1]) ] ) \
		.filter( lambda p: filter_white_init(p[3])) \
                .map( lambda p: p + [ Qlen(p[1]), Qtagnum(p[1]), Qtagnum(p[3]) ] + First(p[3]) )
    #[u'10.188.21.190', u'teredo.ipv6.microsoft.com', 7, u'microsoft.com', 25, 4, 2, u'microsoft', 9, 0.8889, 0, 0.8889, 0]
    data = part.map( lambda p: [p[2], p[4], p[5], p[6], p[8], p[9], p[10], p[11], p[12]] )
    
    min_ = data.reduce( lambda a,b: map_r(a , b, min) )
    max_ = data.reduce( lambda a,b: map_r(a , b, max) )
    min_l, max_l , s_c, l_c = min_[1:], max_[1:], min_[0], max_[0]
    part = part.map( lambda p: (p[0], [([p[1], p[3], p[7]] , m1(p[4:7] + p[8:13]) + m2(p[2])) ]) )
    #(u'10.188.21.190', ([u'teredo.ipv6.microsoft.com', u'microsoft.com', u'microsoft'], [0.261, 0.25, 0.5, 0.25, 0.889, 0.0, 0.889, 0.0, 0.263])),
    
    
    step=0.20
    r1 = part.reduceByKey(lambda a, b: a+b) \
           .map(lambda p: ( p[0], hcluster(p[1], step, 1, distance_func)) ) \
           .map(lambda p: ( p[0], [deal_each_c(i) for i in p[1]]) )
    #r1 = r1.filter(lambda p: filter_result(p[1],10)) #filter1: there should exist at least one cluster whose size is larger than 10.
    #print r1.collect()
    #r1 = r1.map(lambda p:(p[0],p[1][0][4]))
    leastdomains=int(sys.argv[2])
    r1 = r1.map(lambda p:(p[0],filter_cluster(p[1],leastdomains))) #filter2: reject clusters whose size is less than 10(leastdomains) 
    val = r1.map(lambda p: (p[0],p[1][0],p[1][1])).collect()
    print val
    #str=r1.map(lambda p: (print_cluster(p[0],p[1][0],p[1][1],p[1][2]))).collect()
    r1.map(lambda p: insert_mysql(p,a.split('/')[-1])).collect()
    #r1.foreachPartitions(f2).collect()
    #r1.mapPartitions(f).collect()
    print "------------------------------------------------------------------"
    

    #print r1.collect()
    #os.system("rm -rf "+sys.argv[1]+".dir")
    #r1.saveAsTextFile('123.txt')
    exit(0)
