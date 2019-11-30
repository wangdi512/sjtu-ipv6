<?php
$mysql_server_name='deepoceandb'; 
 
$mysql_username='zjc'; 
 
$mysql_password='zjc13120709021'; 
 
$mysql_database='dns'; 
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ; 
mysql_select_db($mysql_database);


$num=$_GET["num"];
#$num=6;
#$time=date('Y-m-d H:i:s');
#echo $time;
//$sql="select t.domain,t.time,t.ip,m.country,m.city from time.domain as t left join  malicious_domain.domain as m on t.main=m.domain where time < '$time'  group by t.domain,t.time,t.ip order by time DESC limit 0,$num";
$sql="select * from log1 order by time DESC limit 0,$num";
$result = mysql_query($sql,$conn);
while($row = mysql_fetch_array($result))
{

$arr[] = array( 
        'domain' => $row['domain'], 
        'time' => $row['time'],
	'ip' => $row['ip'],
	'srcip'=>$row['srcip']
    ); }
echo json_encode($arr);
mysql_close($conn);
?>
