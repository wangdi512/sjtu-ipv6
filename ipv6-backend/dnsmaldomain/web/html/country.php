<?php
$mysql_server_name='deepoceandb';

$mysql_username='zjc';

$mysql_password='zjc13120709021';

$mysql_database='dns';
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ;
mysql_select_db($mysql_database);

$country=$_GET["country"];
$city=$_GET["city"];
#$city='Beijing';
if ($country == null){
	
$coun = (mysql_query("select country from location where location.city = '$city' ",$conn));
$row=mysql_fetch_array($coun);
for($i=0; $row[$i]!= 'None';$i++)
{
	$country=$row[$i];
	break;
	

}
}

$sql="select t.domain,t.time,t.ip,m.city,m.country from dns.log1 as t left join dns.location as m on t.domain=m.domain where m.country ='$country' and t.time < now()  group by t.domain,t.time,t.ip,m.city,m.country order by time desc";
$result = mysql_query($sql,$conn);

while($row = mysql_fetch_array($result))
{

$arr[] = array(
        'domain' => $row['domain'],
	'time' => $row['time'],
	'ip'=>$row['ip'],
        'city' => $row['city'],
	'country' => $row['country'],
    ); }
echo json_encode($arr);
mysql_close($conn);
?>


