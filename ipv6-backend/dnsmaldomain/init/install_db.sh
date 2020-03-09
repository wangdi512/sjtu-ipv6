mysql -uroot -p$MYSQL_ROOT_PASSWORD <<EOF
#dnsmaldomain
source /docker-entrypoint-initdb.d/sql/init.sql
