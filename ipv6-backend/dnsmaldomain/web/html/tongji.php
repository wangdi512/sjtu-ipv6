<?php
date_default_timezone_set("PRC");

$mysql_server_name='deepoceandb'; 
 
$mysql_username='zjc'; 
 
$mysql_password='zjc13120709021'; 
 
$mysql_database='dns'; 
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ; 
mysql_select_db($mysql_database);

$time1=date('m-d',strtotime('-1 day'));
$time2=date('m-d',strtotime('-5 day'));
$sql="select * from tongji order by date desc limit 0,30";
$result = mysql_query($sql,$conn);
while($row = mysql_fetch_array($result))
{

$arr[] = array(
        'date' => $row['date'], 
        'id' => $row['id'],
        'malcount' => $row['malcount'], 
        'logcount' => floor($row['logcount']/100)
    ); }
echo json_encode($arr);
mysql_close($conn);
?>
