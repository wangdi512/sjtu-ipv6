
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from publicsuffixlist import PublicSuffixList
from pyspark import SparkContext

import re
import sys

import MySQLdb

from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.classification import SVMWithSGD, SVMModel

filter_file='/home/ubuntu/dns/deploy/top-10k.txt'
#model_dir ='/home/ubuntu/dns/deploy/tunnel/myDecisionTreeClassificationModel2'
model_dir ='/home/ubuntu/dns/deploy/tunnel/DecisionTreeModel'
#model_dir ='/home/ubuntu/dns/deploy/tunnel/SVMModel'

def filterwhite(x):
  #if len(x)<>8:return False
  #try:
  #  if x[6]:
   #    if len(x[6])<10:
    #      return False
  #except:
  #  return False
  domain=x[6][:-1]
  sf=psl.privatesuffix(domain)
  if sf and sf.count('in-addr.arpa'):return False
  lookup_flag=lookupTable(sf,filterTable.value)
  if lookup_flag==0: return True
  else: return False

def loadTable():
    d={}
    for domain in open(filter_file, "r"):
      domain=domain[:-1]
      d[domain]=1
    return d


def qnamefront(QName,MainDomain):
  if MainDomain == None:md=0
  else:md=len(MainDomain)
  if QName==None:return None
  else:qn=len(QName)
  if qn==md:return None
  return QName[0:(qn-md)-1]


def lookupTable(x, table):
    return table.get(x,0)

def Qlen(QName):
        return len(QName) if QName else 0

def Qtagnum(QName):
        return len(QName.split('.')) if QName else 0

def qnamefront1(QNameFront):
        if QNameFront==None: return 0
        list1='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-'
        for i in QNameFront:
          if i not in list1:
                return 1
        return 0

def qnamefront2(QNameFront):
        if QNameFront==None: return 0
        for i in QNameFront:
          if ord(i)<32 or ord(i)==127:
            return 1
        return 0

def qnamefront3(QNameFront,MainDomain):
        if not QNameFront or not MainDomain: return 0
        if MainDomain.lower()<>MainDomain: return 0
        return 0 if QNameFront.islower() else 1


def asd(x):
        a=x.split(',')[2:]
        b=[]
        for i in a:
                if ']' in i:i=i[:-1]
                i=i.strip()
                tmp=float(i)
                b.append(tmp)
        return b

def insert_mysql(ip,maindomain,details):
  try:
    tablename='tunnel'
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd = "sjtudns", db ="dns")
    c = conn.cursor()
    sql = "insert ignore into "+tablename+"(ip,domain,details)  values(%s,%s,%s)"
    param=(ip,maindomain,details)
    c.execute(sql,param)
    print "insert..."
    conn.commit()
    c.close()
  except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def predict(p):
#return:1 tunnel 0 normal
  count=p[0]
  maxQNameFrontLen=p[16]
  minQNameFrontLen=p[17]
  avgQNameLen=p[12]
  maxQNameTagNum=p[13]
  if count<10: return 0
  if maxQNameFrontLen <= 127: return 0
  if minQNameFrontLen > 13.50:
    if avgQNameLen <= 26.18: return 0
    else:
	if maxQNameTagNum <= 4.5: return 0
	else:return 1
  else:return 0


if __name__ == "__main__":
#    if len(sys.argv) != 2:
#        print("Usage: handle <file>", file=sys.stderr)
#        exit(-1)


    # Initialize the spark context.
   # sc is an existing SparkContext.
    sc = SparkContext(appName="DnsTunnel Detection")
    psl = PublicSuffixList()
    filterTable= sc.broadcast(loadTable())

        # Load a text file and convert each line to a tuple.
    lines = sc.textFile(sys.argv[1])
    parts = lines.map(lambda l: l.split("\t"))
   # Filtering 
    partx = parts.filter(filterwhite)

    #p[6] is domain,p[8] is maindomain,p[9] is qnamefront 
    dnslog = partx.map(lambda p: (p[0], p[1],int(p[2]),int(p[3]),int(p[4]),int(p[5]),p[6][:-1],int(p[7]),psl.privatesuffix(p[6][:-1]),qnamefront(p[6][:-1],psl.privatesuffix(p[6][:-1]))))

    #make dictionary for query maindomain
    #qry=dnslog.map(lambda p:(p[8],p[6])).groupByKey().collectAsMap()
    #for i in  qry.get('qianzhan.com'):
     # print i
    #exit(1)
    
    final_dnslog=dnslog.map(lambda p :([i for i in p] + [Qlen(p[6]),Qtagnum(p[6]),Qlen(p[9]),Qtagnum(p[9]),qnamefront1(p[9]),qnamefront2(p[9]),qnamefront3(p[9],p[8])]))


    schemaString = "TimeStamp ClientIP MsgLength Rcode ANCount ANSize QName QType MainDomain QNameFront"
    fields = [StructField(field_name, IntegerType(), True) for field_name in schemaString.split()]
    fields[0]=StructField('TimeStamp', StringType(), True)
    fields[1]=StructField('ClientIP', StringType(), True)
    fields[6]=StructField('QName', StringType(), True)
    fields[8]=StructField('MainDomain', StringType(), True)
    fields[9]=StructField('QNameFront', StringType(), True)

    addstring='QNameLen QNameTagNum QNameFrontLen QNameFrontTagNum QNameFront1 QNameFront2 QNameFront3'

    fieldsadd=[StructField(field_name, IntegerType(), True) for field_name in addstring.split()]


    final_fields=fields+fieldsadd
    final_schema=StructType(final_fields)

    final_sqlContext = SQLContext(sc)
    final_schemaTunnel = final_sqlContext.createDataFrame(final_dnslog, final_schema)
    final_schemaTunnel.registerTempTable("final_log")
    results = final_sqlContext.sql("SELECT ClientIP,MainDomain, count(*) as v10 ,max(MsgLength) as v11 ,min(MsgLength) as v12,avg(MsgLength) as v13, \
        max(ANCount) as v14,min(ANCount) as v15,avg(ANCount) as v16,max(ANSize) as v17,min(ANSize) as v18,avg(ANSize) as v19,max(QNameLen) as v20,\
        min(QNameLen) as v21,avg(QNameLen) as v22, max(QNameTagNum) as v23,min(QNameTagNum) as v24,avg(QNameTagNum) as v25,max(QNameFrontLen) as v26,\
        min(QNameFrontLen) as v27,avg(QNameFrontLen) as v28, max(QNameFrontTagNum) as v29,min(QNameFrontTagNum) as v30,avg(QNameFrontTagNum) as v31,\
        sum(QNameFront1) as v32,sum(QNameFront1)/count(*)  as v33, sum(QNameFront2) as v34,sum(QNameFront2)/count(*) as v35,sum(QNameFront3) as v36,\
        sum(QNameFront3)/count(*)  as v37\
        FROM final_log group by ClientIP,MainDomain")

    rdd=sc.parallelize(results.collect())
    rdd2=rdd.sortBy(lambda x:(x[0],x[1]))
    rddx=rdd2.map(lambda x:[x.asDict().get(y) for y in sorted(x.asDict().keys())])
    #model = DecisionTreeModel.load(sc, model_dir)    
    #model = SVMModel.load(sc, model_dir)    
    #predictions = model.predict(rddx.map(lambda x:x[2:]))
    predictions = rddx.map(lambda x:predict(x[2:]))
    dataAndPred=rddx.map(lambda x: x).zip(predictions)

    tunnel=dataAndPred.filter(lambda x:x[1]>0.0).map(lambda p:(p[0][0],p[0][1]))
    xlist=tunnel.collect()
    for ip,maindomain in xlist:
      qr = final_sqlContext.sql("SELECT distinct QName FROM final_log where ClientIP='"+ip+"' and MainDomain='"+maindomain+"'")
      details=qr.map(lambda x:x.QName).collect()
      details=','.join(details)
      insert_mysql(ip,maindomain,details)

#RCode,QType,Count,MsgLength(min,avg,max),ANCount(min,avg,max),ANSize(min,avg,max),QNameLen(min,avg,max),QNameTagNum(min,avg,max),QNameFrontLen(min,avg,max),QNameFrontTagNum(min,avg,max),QNameFront1(count,percent),QNameFront2(count,percent),QNameFront3(count,percent)
#RCode-3 QType-7 MsGLength-2 ANCount-4 ANSize-5 QNameLen=Qlen(QName) QNameTagNum=Qtagnum(QName) QNameFrontLen=Qnamefrontlen(QNameFront) QNameFrontTagnum=Qfronttag(QNameFront) QNameFront1=Qfront1(QNameFront) QNameFront2=Qfront2(QNameFront) QNameFront3=Qfront3(QNameFront,MainDomain)

    sc.stop()
