<?php
$mysql_server_name='deepoceandb';

$mysql_username='zjc';

$mysql_password='zjc13120709021';

$mysql_database='dns';
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ;
mysql_select_db($mysql_database);

$sql="select country,count(*) as num from location group by country order by num desc limit 0,6";
$result = mysql_query($sql,$conn);

while($row = mysql_fetch_array($result))
{

$arr[] = array(
      'country' => $row['country'],
	'count' => $row['num']
    ); }
echo json_encode($arr);
mysql_close($conn);
?>

