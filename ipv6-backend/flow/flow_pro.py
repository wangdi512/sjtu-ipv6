import pandas as pd
import os
import time
import json
sjtu_ipv4={'111.186':'0.0/18','175.185':'16.0/20','180.166':'197.0/24','183.195':['251.0/24','252.0/24'],\
'202.112':['26.0/24','27.0/24','28.0/24'],'202.120':['0.0/18','128.0/20'],\
'202.121':'176.0/21','202.127':'242.0/24','210.13':'97.80/28','211.136':'129.96/28','211.144':'125.64/26',\
'211.80':['32.0/19','80.0/20'],'218.193':'176.0/20','219.228':'96.0/19','27.115':'122.0/23',\
'42.247':'16.192/27','58.196':['128.0/19','160.0/20','176.0/23','178.0/24'],\
'58.247':['200.0/24','22.0/24'],'59.78':['0.0/18','112.0/20']}
sjtu_ipv6=['2001:250:6000','2001:251:7801','2001:256:100:2000','2001:DA8:8000',\
'2403:d400','2408:8026:0380']




def cal_time(string1):
	hour=int(string1.split(':')[0])
	minute=int(string1.split(':')[1])
	second=int((string1.split(':')[2]).split('.')[0])
	return hour,minute,second

def convert(n): #ip  ->bin(ip)
	a = n.split(".")
	lst = []
	for i in a:
		two = bin(int(i,10)).lstrip("0b")         #十进制转换成二进制,并去掉开头的0和b,,(根据需要)
		lst.append(two.zfill(8))                  #十进制添加到列表,不足处用0补位
	return "".join(lst)                          #把列表用" "连接起来


class Process():
	def __init__(self,dframe):
		self.data = dframe
		self.ipv4byte_dict={}
		self.ipv6byte_dict={}
		self.serve=[0 for x in range(8) ]
		self.ipv6_updownload_dict={}
		self.ipv4_updownload_dict={}
		self.up_download={}
		self.ipv6server=[0 for x in range(16)]
		'''
		self.ipv6_telecom_dict={} #240e::/18
		self.ipv6_unicom_dict={}  #2408:8000::/20
		self.ipv6_mobile_dict={}  #2409:8000::/20
		self.ipv6_aliyun_dict={}  #2408:4000::/22
		self.ipv6_tecent_dict={}  #240f:4000::/24#
		self.ipv6_baidu_dict={}   #240c:4000::/22
		self.ipv6_amazon_dict={}  #240f:8000::/24
		self.ipv6_education_dict={}  #2001:da8::/31,2001:250::/31;
		'''
		self.byteflow={}

	def total_(self):#all dict -->dataframe 
		columns=['total','ipv4_total','ipv6_total',]
		columns1=['ipv4_web','ipv4_ftp','ipv4_smtp','ipv4_dns','ipv6_web','ipv6_ftp','ipv6_smtp','ipv6_dns']
		columns2=['ipv6_upload','ipv6_download','ipv4_upload','ipv4_download',]
		columns3=['ipv6_upload_telecom','ipv6_upload_aliyun','ipv6_upload_unicom','ipv6_upload_mobile','ipv6_upload_tecent',\
		'ipv6_upload_baidu','ipv6_upload_amazon','ipv6_upload_education']
		total_df=pd.DataFrame(columns=columns)
		service_df=pd.DataFrame(columns=columns1)
		load_df=pd.DataFrame(columns=columns2)
		server_ipv6_df=pd.DataFrame(columns=columns3)


		pass


	def dict1(self,num,type1): #divide flow into different service such as ftp,smtp
		if type1=='ipv4':
			if (self.data.loc[num,'Sport']=='80' or self.data.loc[num,'Sport']== '80') or \
			(self.data.loc[num,'Dport']=='8080' or self.data.loc[num,'Dport']== '8080') or \
			(self.data.loc[num,'Dport']=='443' or self.data.loc[num,'Dport']== '443'):
				self.serve[0]+=self.data.loc[num,'TotBytes']
			elif (self.data.loc[num,'Sport']=='20' or self.data.loc[num,'Sport']== '20') or \
			(self.data.loc[num,'Dport']=='21' or self.data.loc[num,'Dport']== '21'):
				self.serve[1]+=self.data.loc[num,'TotBytes']
			elif (self.data.loc[num,'Sport']=='25' or self.data.loc[num,'Sport']== '25'):
				self.serve[2]+=self.data.loc[num,'TotBytes']
			elif (self.data.loc[num,'Sport']=='53' or self.data.loc[num,'Sport']== '53'):
				self.serve[3]+=self.data.loc[num,'TotBytes']
		if type1=='ipv6':
			if (self.data.loc[num,'Sport']=='80' or self.data.loc[num,'Sport']== '80') or \
			(self.data.loc[num,'Dport']=='8080' or self.data.loc[num,'Dport']== '8080') or \
			(self.data.loc[num,'Dport']=='443' or self.data.loc[num,'Dport']== '443'):
										
				self.serve[4]+=self.data.loc[num,'TotBytes']
			elif (self.data.loc[num,'Sport']=='20' or self.data.loc[num,'Sport']== '20') or \
				(self.data.loc[num,'Dport']=='21' or self.data.loc[num,'Dport']== '21'):
				self.serve[5]+=self.data.loc[num,'TotBytes']
			elif (self.data.loc[num,'Sport']=='25' or self.data.loc[num,'Sport']== '25'):
				self.serve[6]+=self.data.loc[num,'TotBytes']
			elif (self.data.loc[num,'Sport']=='53' or self.data.loc[num,'Sport']== '53'):
				self.serve[7]+=self.data.loc[num,'TotBytes']


	'''
	def adddict(self,num,key,dict1,matching_rule,type): 
	#divide ipv6 flow into different service such as telecom except eaucation because education has two network segment 
		if type=='upload':   #upload srcip=sjtu_ipv6,so we need to divide and sum dstip 
			if (self.data.loc[num,'DstAddr'].lower()).find(matching_rule) !=-1:   #rule means Network segment of the server 
				if dict1.__contains__(key) :
					dict1[key]=dict1[key]+self.data.loc[num,'TotBytes']
				else:
					dict1[key]=self.data.loc[num,'TotBytes']
		elif type =='download':
			if (self.data.loc[num,'SrcAddr'].lower()).find(matching_rule) !=-1:
				if dict1.__contains__(key) :
					dict1[key]=dict1[key]+self.data.loc[num,'TotBytes']
				else:
					dict1[key]=self.data.loc[num,'TotBytes']
				pass


	def dict4(self,num,key,type): #to divide ipv6 flow into different server such as telecom,unicom,mobile
		flag='non'
		if type=='upload' and flag=='non':
			if (self.data.loc[num,'DstAddr'].lower()).find('2001:da8') !=-1 or \
				(self.data.loc[num,'DstAddr'].lower()).find('2001:250') !=-1:  #eaucation web
				flag='edu'
				if self.ipv6_education_dict.__contains__(key) :
						self.ipv6_education_dict[key]=self.ipv6_education_dict[key]+self.data.loc[num,'TotBytes']
				else:
					self.ipv6_education_dict[key]=self.data.loc[num,'TotBytes']
				pass
		elif type == 'download' and flag=='non':
			if (self.data.loc[num,'SrcAddr'].lower()).find('2001:da8') !=-1 or \
				(self.data.loc[num,'SrcAddr'].lower()).find('2001:250') !=-1:  #eaucation web
				flag='edu'
				if self.ipv6_education_dict.__contains__(key) :
						self.ipv6_education_dict[key]=self.ipv6_education_dict[key]+self.data.loc[num,'TotBytes']
				else:
					self.ipv6_education_dict[key]=self.data.loc[num,'TotBytes']
				pass
		if flag=='non':
			self.adddict(num,key,self.ipv6_telecom_dict,'240e',type) #telecom_dict
			self.adddict(num,key,self.ipv6_unicom_dict,'2408:8',type) #unicom_dict
			self.adddict(num,key,self.ipv6_mobile_dict,'2409:8',type) #mobile_dict
			self.adddict(num,key,self.ipv6_aliyun_dict,'2408:4',type) #aliyun_dict
			self.adddict(num,key,self.ipv6_tecent_dict,'240f:40',type) #tecent_dict
			self.adddict(num,key,self.ipv6_baidu_dict,'240c:4',type) #baidu_dict
			self.adddict(num,key,self.ipv6_amazon_dict,'240f:80',type) #amazon_dict

	'''

	def server_list(self,num,type):
		if type=='upload':
			if (self.data.loc[num,'DstAddr'].lower()).find('2001:da8') !=-1 or \
			(self.data.loc[num,'DstAddr'].lower()).find('2001:250') !=-1:
				self.ipv6server[0]=self.ipv6server[0]+self.data.loc[num,'TotBytes']  #eaucation web
				
			elif (self.data.loc[num,'DstAddr'].lower()).find('240e') !=-1:
				self.ipv6server[1]=self.ipv6server[1]+self.data.loc[num,'TotBytes'] #telecom_dict
			elif (self.data.loc[num,'DstAddr'].lower()).find('2408:8') !=-1:
				self.ipv6server[2]=self.ipv6server[2]+self.data.loc[num,'TotBytes'] #unicom
			elif (self.data.loc[num,'DstAddr'].lower()).find('2409:8') !=-1:
				self.ipv6server[3]=self.ipv6server[3]+self.data.loc[num,'TotBytes']  #mobile
			elif (self.data.loc[num,'DstAddr'].lower()).find('2408:4') !=-1:
				self.ipv6server[4]=self.ipv6server[4]+self.data.loc[num,'TotBytes']   #aliyun
			elif (self.data.loc[num,'DstAddr'].lower()).find('240f:40') !=-1:
				self.ipv6server[5]=self.ipv6server[5]+self.data.loc[num,'TotBytes']   #tencent
			elif (self.data.loc[num,'DstAddr'].lower()).find('240c:4') !=-1:                                
				self.ipv6server[6]=self.ipv6server[6]+self.data.loc[num,'TotBytes']   #baidu
			elif (self.data.loc[num,'DstAddr'].lower()).find('240f:80') !=-1:
				self.ipv6server[7]=self.ipv6server[7]+self.data.loc[num,'TotBytes']   #amazon
		if type=='download':
			if (self.data.loc[num,'SrcAddr'].lower()).find('2001:da8') !=-1 or \
			(self.data.loc[num,'SrcAddr'].lower()).find('2001:250') !=-1:
				self.ipv6server[8]=self.ipv6server[8]+self.data.loc[num,'TotBytes']  #eaucation web

			elif (self.data.loc[num,'SrcAddr'].lower()).find('240e') !=-1:
				self.ipv6server[9]=self.ipv6server[9]+self.data.loc[num,'TotBytes'] #telecom_dict
			elif (self.data.loc[num,'SrcAddr'].lower()).find('2408:8') !=-1:
				self.ipv6server[10]=self.ipv6server[10]+self.data.loc[num,'TotBytes'] #unicom
			elif (self.data.loc[num,'SrcAddr'].lower()).find('2409:8') !=-1:
				self.ipv6server[11]=self.ipv6server[11]+self.data.loc[num,'TotBytes']  #mobile
			elif (self.data.loc[num,'SrcAddr'].lower()).find('2408:4') !=-1: 
				self.ipv6server[12]=self.ipv6server[12]+self.data.loc[num,'TotBytes']   #aliyun
			elif (self.data.loc[num,'SrcAddr'].lower()).find('240f:40') !=-1:
				 self.ipv6server[13]=self.ipv6server[13]+self.data.loc[num,'TotBytes']   #tencent
			elif (self.data.loc[num,'SrcAddr'].lower()).find('240c:4') !=-1:                                                      
				self.ipv6server[14]=self.ipv6server[14]+self.data.loc[num,'TotBytes']   #baidu
			elif (self.data.loc[num,'SrcAddr'].lower()).find('240f:80') !=-1:                                
				self.ipv6server[15]=self.ipv6server[15]+self.data.loc[num,'TotBytes']   #amazon


	def dict2(self,dict1,key,num,dict2=sjtu_ipv4,type='ipv4'): #to divide upload and download 
		upload_key=key+'_upload'
		download_key=key+'_download'
		if type=='ipv6':
			for ipv6 in sjtu_ipv6:
				if self.data.loc[num,'SrcAddr'].find(ipv6) !=-1: #upload ipv6 flow
					self.server_list(num,'upload') #divide server of ipv6
					if dict1.__contains__(upload_key) :
						dict1[upload_key]=dict1[upload_key]+self.data.loc[num,'TotBytes']
					else:
						dict1[upload_key]=self.data.loc[num,'TotBytes']
				elif self.data.loc[num,'DstAddr'].find(ipv6) !=-1:  #download ipv6 flow
					self.server_list(num,'download')
					if dict1.__contains__(download_key) :
						dict1[download_key]=dict1[download_key]+self.data.loc[num,'TotBytes']
					else:
						dict1[download_key]=self.data.loc[num,'TotBytes']
		elif type == 'ipv4':
			srckeylist=self.data.loc[num,'SrcAddr'].split('.') #202.120.1.65->202 120 1 65
			srckey1=srckeylist[0]+'.'+srckeylist[1]  #202.120
			srckey2=srckeylist[2]+'.'+srckeylist[3]  #1.65
			dstkeylist=self.data.loc[num,'DstAddr'].split('.') #202.120.1.65->202 120 1 65
			dstkey1=dstkeylist[0]+'.'+dstkeylist[1]  #202.120
			dstkey2=dstkeylist[2]+'.'+dstkeylist[3]  #1.65


			if dict2.__contains__(srckey1):
				if isinstance(dict2[srckey1],list):
					for i in range(len(dict2[srckey1])):  #the value of the key maye a list
						mask_num = int(dict2[srckey1][i].split('/')[1])-16  
						sjtu_ip = dict2[srckey1][i].split('/')[0]
						if convert(sjtu_ip)[0:mask_num] == convert(srckey2)[0:mask_num]:   #belong to this sjtu_ip
							if dict1.__contains__(upload_key) :
								dict1[upload_key]=dict1[upload_key]+self.data.loc[num,'TotBytes']
							else:
								dict1[upload_key]=self.data.loc[num,'TotBytes']
				elif isinstance(dict2[srckey1],str):
					mask_num = int(dict2[srckey1].split('/')[1])-16  
					sjtu_ip = dict2[srckey1].split('/')[0]
					if convert(sjtu_ip)[0:mask_num] == convert(srckey2)[0:mask_num]:   #belong to this sjtu_ip
						if dict1.__contains__(upload_key) :
							dict1[upload_key]=dict1[upload_key]+self.data.loc[num,'TotBytes']
						else:
							dict1[upload_key]=self.data.loc[num,'TotBytes']

					pass

			elif dict2.__contains__(dstkey1):
				#print(dict2[dstkey1])
				#print(type(dict2[dstkey1]))
				if isinstance(dict2[dstkey1],list):#type(dict2[dstkey1])==list:
					for i in range(len(dict2[dstkey1])):  #the value of the key maye a list
						mask_num = int(dict2[dstkey1][i].split('/')[1])-16  
						sjtu_ip = dict2[dstkey1][i].split('/')[0]
						if convert(sjtu_ip)[0:mask_num] == convert(dstkey2)[0:mask_num]:   #belong to this sjtu_ip
							if dict1.__contains__(download_key) :
								dict1[download_key]=dict1[download_key]+self.data.loc[num,'TotBytes']
							else:
								dict1[download_key]=self.data.loc[num,'TotBytes']
				elif isinstance(dict2[dstkey1],str):
					mask_num = int(dict2[dstkey1].split('/')[1])-16  
					sjtu_ip = dict2[dstkey1].split('/')[0]
					if convert(sjtu_ip)[0:mask_num] == convert(dstkey2)[0:mask_num]:   #belong to this sjtu_ip
						if dict1.__contains__(download_key) :
							dict1[download_key]=dict1[download_key]+self.data.loc[num,'TotBytes']
						else:
							dict1[download_key]=self.data.loc[num,'TotBytes']


	def test(self):
		ipv6_df=pd.DataFrame(columns=self.data.columns) #store  all ipv6 dataframe lines
		#print(self.data.shape[0])
		'''
		ipv4byte_dict={}
		ipv6byte_dict={}
		ipv4_web_dict={}
		ipv4_ftp_dict={}
		ipv4_smtp_dict={}
		ipv4_dns_dict={}
		ipv6_web_dict={}
		ipv6_ftp_dict={}
		ipv6_smtp_dict={}
		ipv6_dns_dict={}
		ipv6_updownload_dict={}
		ipv4_updownload_dict={}
		'''
		byte_num=0

		#print(type(self.data.loc[0,'Dport']))
		for i in range(self.data.shape[0]):
			#print(type(self.data.loc[0,'TotBytes']))
			hour,minute,second=cal_time(self.data.loc[i,'StartTime'])
			key=str(hour)+":"+str(minute)+':'+str(second) #Timestamp
			srcip=self.data.loc[i,'SrcAddr']
			dstip=self.data.loc[i,"DstAddr"]

			if (":" in srcip or ":" in dstip):   #divide into ipv4 and ipv6
				ipv6_df=ipv6_df.append(self.data.loc[i,:])
				self.dict1(i,'ipv6')    #divide into different services:web,ftp and  smtp
				self.dict2(self.ipv6_updownload_dict,key,i,sjtu_ipv6,'ipv6')
				if self.ipv6byte_dict.__contains__(key) :
					self.ipv6byte_dict[key]=self.ipv6byte_dict[key]+self.data.loc[i,'TotBytes']     #if key has time,sum it ,if not ,create new key t
				else:
					self.ipv6byte_dict[key]=self.data.loc[i,'TotBytes']
			else:
				self.dict1(i,'ipv4')
				self.dict2(self.ipv4_updownload_dict,key,i,sjtu_ipv4,'ipv4')
				if self.ipv4byte_dict.__contains__(key) :
					self.ipv4byte_dict[key]=self.ipv4byte_dict[key]+self.data.loc[i,'TotBytes']
				else:
					self.ipv4byte_dict[key]=self.data.loc[i,'TotBytes']	
		
		#print(self.ipv4byte_dict)
		#print('ok')
		'''
		df1=pd.DataFrame(columns=self.df.columns)
		for x in range(0,1000):
			df1.append(dict(self.df.iloc[0,:]),ignore_index=True)
			pass
		#print(df1)
		df1.to_csv('3.flow',sep='\t')
		'''
	def get_result(self):
		#print(self.ipv4byte_dict)
		#print(self.ipv6byte_dict)
		total_flow=[0,0] #total_flow:[ipv4_total,ipv6_total]
		keys=list(set(list(self.ipv4byte_dict.keys())+list(self.ipv6byte_dict.keys())))
		#print(keys)
		for key in keys:
			self.byteflow[key]=[0,0]
			self.up_download[key]=[0,0,0,0]
			pass
		#self.byteflow[key]=[0,0]  for key in keys
		#self.up_download[key]=[0,0,0,0] for key in keys
		for key in keys:  #return chart 1 return ipv4 and v6 flow byte in every second;chart2 total ipv4 and ipv6
			upkey=key+'_upload'#return chart 4 return key:time value:[ipv4_upload,ipv4_download,ipv6_upload,ipv6_download]
			downkey=key+'_download'

			#byte_flow
			if self.ipv4byte_dict.__contains__(key):
				self.byteflow[key][0]=self.byteflow[key][0]+self.ipv4byte_dict[key]
				total_flow[0]=total_flow[0]+self.ipv4byte_dict[key]
			if self.ipv6byte_dict.__contains__(key):
				self.byteflow[key][1]=self.byteflow[key][1]+self.ipv6byte_dict[key]
				total_flow[1]=total_flow[1]+self.ipv6byte_dict[key]


			#updownload flow 
			if self.ipv4_updownload_dict.__contains__(upkey):
				self.up_download[key][0]+=self.ipv4_updownload_dict[upkey]
			if self.ipv4_updownload_dict.__contains__(downkey):
				self.up_download[key][1]+=self.ipv4_updownload_dict[downkey]
			if self.ipv6_updownload_dict.__contains__(upkey):
				self.up_download[key][2]+=self.ipv6_updownload_dict[upkey]
			if self.ipv6_updownload_dict.__contains__(downkey):
				self.up_download[key][3]+=self.ipv6_updownload_dict[downkey]

		'''
		print(self.byteflow)    #{'timestamp': [ipv4_byte,ipv6_byte]}每秒ipv4，v6流量
		print(total_flow)     #[ipv4,ipv6] 总的ipv4，ipv6流量
		print(self.serve) [ipv4_http,ipv4_ftp,ipv4_smtp,ipv4_dns,ipv6_http,ipv6_ftp,ipv6_smtp,ipv6_dns] 
		总的ipv4，v6提供的服务字节数，len(数组)=4(服务)*2(v4,v6)=8
		print(self.up_download) {'timestamp' :[ipv4_upload,ipv4_download,ipv6_upload,ipv6_download]}
		每秒ipv4与v6的上下行
		print(self.ipv6server) [7个服务提供商上行byte，七个服务提供商下行byte]，即[byte*14]
		教育网，中国电信，联通，移动，阿里，腾讯，亚马逊提供的上下行
		'''
		#print(self.byteflow,self.up_download,total_flow,self.serve,self.ipv6server)
		return self.byteflow,self.up_download,total_flow,self.serve,self.ipv6server
		
		

	def write_csv(self,path):
		self.data.to_csv(path,sep='\t')



if __name__ == '__main__':
	start=time.clock()
	dframe = pd.read_csv("ipv4_6.flow",sep='\s+')
	dframe=dframe.dropna(axis=0, how='any')
	dframe=dframe.reset_index(drop=True)
	a = Process(dframe)
	#print(time.clock()-start)
	a.test()
	byte_flow,up_download,total_flow,serve,ipv6server=a.get_result()
	print(byte_flow)
	print(up_download)
	print(total_flow)
	print(serve)
	print(ipv6server)
	print(time.clock()-start)
	list1={'chart1':byte_flow,'chart2':up_download,'chart3':total_flow,'chart4':serve,'chart5':ipv6server}
	dict1={'data':list1}
	json_str = json.dumps(dict1, indent=3)
	with open('1540.json','w+') as f:
		f.write(json_str)
