'''
Fast-Flux
  dump pickle
  filter
  final for 
'''

from pyspark.sql import SQLContext
from pyspark.sql.types import *
from publicsuffixlist import PublicSuffixList
from pyspark import SparkContext

from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.regression import LabeledPoint

import re
import sys
import pygeoip
import os
import shutil
import cPickle as pickle
import shutil
import numpy as np
import MySQLdb

std_default_value=0.6
#unit:minutes
time_duration=180


filter_file='/home/ubuntu/dns/deploy/top-10k.txt'
geo_asn_file='/home/ubuntu/dns/deploy/GeoIPASNum.dat'
geo_city_file='/home/ubuntu/dns/deploy/GeoLiteCity.dat'
his_dir='/home/ubuntu/dns/deploy/flux/history/'
#for test
his_feature_file='/home/ubuntu/dns/deploy/flux/history_feature.txt'
his_tmp_feature_file='/tmp/history_feature'

def usage():
  if len(sys.argv)<3:
    print "Usage:"

def filterwhite(x):
  domain=x[0]
  sf=psl.privatesuffix(domain)
  lookup_flag=lookupTable(sf,filterTable.value)
  if lookup_flag==0: return True
  else: return False

def lookupTable(x, table):
    return table.get(x,0)

def loadTable():
    d={}
    for domain in open(filter_file, "r"):
      domain=domain[:-1]
      d[domain]=1
    return d
  
def Qlen(QName):
  return len(QName) if QName else 0

def iplist(s):
  a=s.split(';')
  t=[]
  for i in a:
    if i.split(',')[0]=='':
      break
    t.append(i.split(',')[0])
    
  return list(set(t))

def ac(ipl,tp,li):
  results=[]
  ASN=pygeoip.GeoIP(geo_asn_file)
  CITY=pygeoip.GeoIP(geo_city_file)
  if tp=='asn':
    for i in ipl:
      asn=ASN.org_by_addr(str(i))
      if asn not in results:
        results.append(asn)
      
  else:
    for i in ipl:
      if i=='':
        break
      if CITY.record_by_addr(str(i))==None:
        break
      city=CITY.record_by_addr(str(i))['city']
      if city not in results:
        results.append(city)

  if li=='list':
    return results
  else:
    return len(results) 

def ttl(ipttl):
  a=ipttl.split(';')
  t=0
  for i in a:
    if i =='':
      break
    b=int(i.split(',')[1])
    if b >t:
      t=b
  return t

def num2416ip(ipl,tp,li):

  results=[]
  if tp==24:
    for i in ipl:
      if i=='':
        break
      ip24=i.rsplit('.',1)[0]
      if ip24 not in results:
        results.append(ip24)
  else:
    for i in ipl:
      if i=='':
        break
      ip16=i.rsplit('.',2)[0]
      if ip16 not in results:
        results.append(ip16)    
  if li=='list':
    return results
  else:
    return len(results)   

def read_history(new_history,flag):
  history=sc.parallelize(new_history)
  #history:domain,(singleipnum,iplist,asnlist,citylist,24numlist,16numlist)
  #output singleipnum,len(ip),fluxiness,len(asnlist),len(citylist),len(24numlist),len(16numlist)
  history_count=history.map(lambda p:(p[0],len(p[1][1]),len(p[1][1])/float(p[1][0]),len(p[1][2]),len(p[1][3]),len(p[1][4]),len(p[1][5]))) 
  history_list=history
  # write tmp file for test
  if flag:
    if os.path.exists(his_tmp_feature_file):
       shutil.rmtree(his_tmp_feature_file,True)
    history_count.repartition(1).saveAsTextFile('file://'+his_tmp_feature_file)
    if os.path.exists(his_feature_file):
       os.remove(his_feature_file)
    fp=open(his_feature_file,'w')
    fp.write("'domain', 'len(ip)', 'fluxiness', 'len(asnlist)', 'len(citylist)', 'len(24numlist)', 'len(16numlist)'\n")
    for line in open(his_tmp_feature_file+"/part-00000").readlines():
       fp.write(line)
    fp.close()
    
         
  return history_count,history_list

def output_flux(history_count,singlelog):
  #singlelog.join(history_count)-->if existed: ret fast_flux_domain  else: naivebayes.predict(singlog):fast_flux_domain if existed else ""
  return ""

def max(a,b):
  return a if a>=b else b

def distinct(x):
  return list(set(x))

def loadMonitorDomain():
    d={}
    for domain in open("/home/ubuntu/test/mondomain.txt", "r"):
      domain=domain[:-1]
      d[domain]=1
    return d

     
def filterdomain(x):
   domain=x[0]
   lookup_flag= filterDomain.value.get(domain,0)
   if lookup_flag==1: return True
   else: return False  

def count_std_mean(x,y):
   a=np.array(x)
   b=np.array(y)
   c=a-b
   return np.std(c)

def insert_mysql(domain,iplist,std_value,flag=1):
  try:
    tablename='fastflux'
    details=','.join(iplist)
    score=str(std_value)
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd = "sjtudns", db ="dns")
    c = conn.cursor()
    sql='select * from '+tablename+' where domain=%s'
    param=(domain)
    count=c.execute(sql,param)
    print "count=",count
    if count<>0:
      sql = "update "+tablename+" set details=%s,score=%s where domain=%s"
      param=(details,score,domain)
      c.execute(sql,param)
      print "update..."
    else:
      sql = "insert ignore into "+tablename+"(domain,details,score)  values(%s,%s,%s)"
      param=(domain,details,score)
      c.execute(sql,param)
      print "insert..."
    conn.commit()
    c.close()
  except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def predict(p):
#return: 1 fastflux 0 normal
    domainlen,iplen,asnnum,citynum,net24ip,net16ip,ttl=p[0],p[1],p[2],p[3],p[4],p[5],p[6]
    if ttl<=600 and iplen>=4 and asnnum>=2:
    #    print "domainlen,iplen,asnnum,citynum,net24ip,net16ip,ttl:",domainlen,iplen,asnnum,citynum,net24ip,net16ip,ttl 
	return 1
    else: return 0 

  
if __name__ == "__main__":
    sc = SparkContext(appName="Fast-Flux")
    psl = PublicSuffixList()
    filterTable= sc.broadcast(loadTable())
    ###get monitored domain for test--service for these domains only! 
    #filterDomain= sc.broadcast(loadMonitorDomain())

    #####################
    try:
      f2=file(his_dir+'history.pickle','r')
      new_history=pickle.load(f2)
      f2.close()
    except:
      print "this is a new pickle file"
      new_history=[]
      tuple=('nonexisteddomain',(1,[],[],[],[],[]))
      new_history.append(tuple)

    #history_count,history_list=read_history(new_history,1) 1-write tmpfile for test
    history_count,history_list=read_history(new_history,0)

    data=sys.argv[1]

    # 1 Single Length of IP List
    lines = sc.textFile('file://'+data)
    #timestamp domain Aip
    parts = lines.map(lambda l: l.split("\t"))
    #domain Aip
    partx = parts.map(lambda p:(p[1][:-1],p[2]))
    partx = partx.filter(filterwhite)
    ###filtering for test
    #partx = partx.filter(filterdomain)

    #domain Aip iplist
    partx=partx.map(lambda p: ([i for i in p ]+[iplist(p[1])]))
    #output single feature: domain,(ipttl,iplist),qlen,len(iplist),asn_num,city_num,num24,num16,ttl
    singlelog=partx.map(lambda p: ([i for i in p ]+[Qlen(p[0]),len(p[2]),ac(p[2],'asn','num'),ac(p[2],'city','num'),num2416ip(p[2],24,'num'),num2416ip(p[2],16,'num'),ttl(p[1])]))
    # Load model
    svmModel = SVMModel.load(sc, "file:///home/ubuntu/dns/deploy/flux/SVMModel")
    #result=singlelog.map(lambda p:p[3:]).take(3)
    result=singlelog.map(lambda p:(p[0],p[2],svmModel.predict(p[3:]))).filter(lambda x:x[2]<>0)
    #result=singlelog.map(lambda p:(p[0],p[2],predict(p[3:]))).filter(lambda x:x[2]<>0)
    #print result.collect()
    # output the fast-flux domain with machine learning and history info.
##      singlelog.repartition(1).saveAsTextFile('file://'+data+'_f')
    #score=output_flux(history_count,singlelog)
    
   # 2 History Pickle
    #Domain IPTTL IPList(p[2]) DLen IPNum ASNNum ASNList(p[5][1]) CITYNum CITYList Num24 Num24List Num16 Num16List TTL
    Rlog=partx.map(lambda p: ([i for i in p ]+[Qlen(p[0]),len(p[2]),(ac(p[2],'asn','num'),ac(p[2],'asn','list')),(ac(p[2],'city','num'),ac(p[2],'city','list')),(num2416ip(p[2],24,'num'),num2416ip(p[2],24,'list')),(num2416ip(p[2],16,'num'),num2416ip(p[2],16,'list')),ttl(p[1])]))
 #domain,single length,iplist,asnlist,citylist,24numlist,16numlist
    Rloghis=Rlog.map(lambda p:(p[0],(len(p[2]),p[2],p[5][1],p[6][1],p[7][1],p[8][1]))) #There don't consider TTL because it makes nonsense.
      #print Rloghis.top(3)
    history1=history_list+Rloghis 
      #print history1.top(3)
    history=history1.reduceByKey(lambda a,b:(max(a[0],b[0]),distinct(a[1]+b[1]),distinct(a[2]+b[2]),distinct(a[3]+b[3]),distinct(a[4]+b[4]),distinct(a[5]+b[5])))
    #print history.top(3)
    f=file(his_dir+'history.pickle','w')
    pickle.dump(history.collect(),f)
    f.close()

   # 3 Insert mysql with malicous score
   #RDD: result history history_list 
  #  qry=history_list.map(lambda p:(p[0],p[1])).collectAsMap()
    new_history_count=history.map(lambda p:(p[0],len(p[1][1]),len(p[1][1])/float(p[1][0]),len(p[1][2]),len(p[1][3]),len(p[1][4]),len(p[1][5])))
    std_value=new_history_count.map(lambda p:(p[0],p[1:])).join(history_count.map(lambda p:(p[0],p[1:]))).mapValues(lambda (a,b):count_std_mean(a,b)) \
       .collectAsMap()
    result.map(lambda p:insert_mysql(p[0],p[1],std_value.get(p[0]))).collect()
    #result.map(lambda p:insert_mysql(p[0],p[1],std_value.get(p[0]),1) if qry.get(p[0],0)<>0 else insert_mysql(p[0],p[1],std_default_value,0)).collect()
    #result.map(lambda p:insert_mysql(p[0],p[1],std_default_value,0)).collect()
   # print result.map(lambda p:(p[0],p[1],std_default_value,0)).collect()

    print '============Done============='

