import MySQLdb
db = MySQLdb.connect('deepoceandb','zjc','zjc13120709021','dns')
cursor = db.cursor()
sql = "select * from tongji where date = '%s' and id = '%s'"%('05-19','0:00')
cursor.execute(sql)
result = cursor.fetchall()
print result
