<?php
date_default_timezone_set("PRC");

$mysql_server_name='deepoceandb'; 
 
$mysql_username='zjc'; 
 
$mysql_password='zjc13120709021'; 
 
$mysql_database='dns'; 
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ; 
mysql_select_db($mysql_database);

$sql="select * from systime";
$result = mysql_query($sql,$conn);
while($row = mysql_fetch_array($result))
{
$arr[] = array(
        'year' => $row['year'], 
        'month' => $row['month'],
        'day' => $row['day'], 
        'hour' => $row['hour'],
	'minute' => $row['minute'],
	'second' => $row['second']
    ); 
}
echo json_encode($arr);
mysql_close($conn);
?>
