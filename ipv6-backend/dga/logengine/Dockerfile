FROM ubuntu:16.04
ADD ./pyramid /root/logengine/pyramid

RUN apt-get update
RUN apt-get install -y python-pip && apt-get install -y gcc && apt-get install -y make && apt-get install -y libssl-dev && apt-get install -y libpcap-dev  
RUN pip install schedule
RUN cd /root/logengine/pyramid/pdns && tar zxvf ldns-1.7.0.tar.gz 
RUN cd /root/logengine/pyramid/pdns/ldns-1.7.0 && ./configure --disable-dane-verify && make && make install 
RUN cd /root/logengine/pyramid/pdns/pdns3new && make && cp pdns3new ../../bin/.
RUN cd /root/logengine/pyramid/pdns/pdns_all2 && make && cp pdns_all2 ../../bin/. 
RUN cd /root/logengine/pyramid/pdns/pdns && make && cp pdns ../../bin/. 
RUN cd /root/logengine/pyramid/pdns/pdns_resp && make && cp pdns_resp ../../bin/. 
RUN echo "/usr/local/lib/libldns.so.2" >> /etc/ld.so.conf && ldconfig
RUN cp /root/logengine/pyramid/bin/* /usr/bin/.
RUN apt-get install -y tzdata
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
RUN mkdir /root/logengine/runlog
WORKDIR /root/logengine
ADD ./pcapfile /root/logengine/pcapfile
