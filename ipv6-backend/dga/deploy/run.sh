INPUTDIR=/log/dga_20160418_09
hadoop fs -ls file:///home/spark/...
tun_%Y%m%d_%H%M.log
dga_%Y%m%d_%H%M.log
flux_%Y%m%d_%H%M.log
interval 5 minutes

spark-submit --master local[*] /home/ubuntu/dns/deploy/dga/dga3.py $INPUTDIR 20

# one hour
spark-submit --master local[*] /deploy/dga/dga3.py /log//dga_20160417_00/ 20
