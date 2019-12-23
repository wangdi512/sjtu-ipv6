import pandas as pd
import os
import time
sjtu_ipv4={'111.186':'0.0/18','175.185':'16.0/20','180.166':'197.0/24','183.195':['251.0/24','252.0/24'],\
'202.112':['26.0/24','27.0/24','28.0/24'],'202.120':['0.0/18','128.0/20'],\
'202.121':'176.0/21','202.127':'242.0/24','210.13':'97.80/28','211.136':'129.96/28','211.144':'125.64/26',\
'211.80':['32.0/19','80.0/20'],'218.193':'176.0/20','219.228':'96.0/19','27.115':'122.0/23',\
'42.247':'16.192/27','58.196':['128.0/19','160.0/20','176.0/23','178.0/24'],\
'58.247':['200.0/24','22.0/24'],'59.78':['0.0/18','112.0/20']}
sjtu_ipv6=['2001:250:6000','2001:251:7801','2001:256:100:2000','2001:DA8:8000',\
'2403:d400','2408:8026:0380']



start=time.clock()
dframe = pd.read_csv("1.flow",sep='\s+')
dframe=dframe.dropna(axis=0, how='any')
dframe=dframe.reset_index(drop=True)
dframe1=pd.read_csv("1540.csv",sep=',')
#print(dframe.iloc[1,:])
#print(dframe1.loc[1,:])
dict1={}
dict1['Dur']=0
dict1['Proto']=6
dict1['Dir']='<>'
for i in range(len(dframe1)-3):
    dict1['StartTime']=dframe1.loc[i,'ts'].split(' ')[1]
    dict1['SrcAddr']=dframe1.loc[i,'sa']
    dict1['DstAddr']=dframe1.loc[i,'da']
    dict1['Sport']=dframe1.loc[i,'sp']
    dict1['Dport']=dframe1.loc[i,'dp']
    dict1['TotBytes']=dframe1.loc[i,'ibyt']
    dict1['TotPkts']=dframe1.loc[i,'ipkt']
    dframe=dframe.append(dict1,ignore_index=True)
    #dict
    #print(dict1)
    pass
dframe.to_csv('test.csv',index=False)
drame3=pd.read_csv('test.csv',sep=',')
print(drame3.loc[1,:])
#print(dframe1.iloc[1,:])
#print(time.clock()-start)
#print(a.get_result())
