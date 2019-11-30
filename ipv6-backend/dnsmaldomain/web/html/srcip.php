<?php
$mysql_server_name='deepoceandb'; 
 
$mysql_username='zjc'; 
 
$mysql_password='zjc13120709021'; 
 
$mysql_database='dns'; 
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ; 
mysql_select_db($mysql_database);


$srcip = $_GET["srcip"];
#$num=6;
#$time=date('Y-m-d H:i:s');
#echo $time;
$sql="select * from amallog where srcip = '$srcip' order by time DESC limit 0,100";
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
