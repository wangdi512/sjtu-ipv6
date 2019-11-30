pdns:  pdns -i packet.pcap 产生rr一个log 自动命名 通过dnscache.h保证10分钟内去重 只有来自权威记录dnspkt.h逻辑控制 60mins
pdns_resp:  pdns_resp -i packet.pcap 产生resp一个log 自动命名 60mins
pdns_all2: pdns_all2 -i packet.pcap 产生全流量三个log,rr_,qry_,resp_, 自动命名 其中resp不含有解析结果 10mins
pdns3new:  pdns3new -i packet.pcap 产生dga,tunnel,flux三个log 自动命名 5mins
argus: argus -r p.pcap -w -|ra -r - -s stime dur proto saddr dir daddr sport dport bytes pkts -w p.flow 全名取pcap文件前缀
