<?php
date_default_timezone_set("PRC");

$mysql_server_name='deepoceandb';

$mysql_username='zjc';

$mysql_password='zjc13120709021';

$mysql_database='dns';
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ;
mysql_select_db($mysql_database);
$time1=date('Y-m-d');
$time2=date('Y-m-d H:i:s');

$sql = "select  count(*) as num  from log1  where time  between '$time1' and '$time2' ";
$result = mysql_query($sql,$conn);
$row = mysql_fetch_array($result)[0];
$sql = "select count(*) as num from log1";
$result = mysql_query($sql,$conn);
$total = mysql_fetch_array($result)[0];
$sql = "select * from logcount where logtype='log'";
$result = mysql_query($sql,$conn);
$totallog = mysql_fetch_array($result)[1];
echo json_encode([$row,$total,$totallog]);
mysql_close($conn);
?>



