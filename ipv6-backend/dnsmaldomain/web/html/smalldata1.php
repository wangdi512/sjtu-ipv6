<?php
$mysql_server_name='deepoceandb';

$mysql_username='zjc';

$mysql_password='zjc13120709021';

$mysql_database='smalldata';
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ;
mysql_select_db($mysql_database);

$num=$_GET["num"];
#$domain=$_GET["domain"];
$sql="select * from  data where num='$num'";
$result = mysql_query($sql,$conn);
while($row = mysql_fetch_array($result))
{

$arr[] = array(
        'domain' => $row['domain'],
        'value' => $row['value'],
        'num' => $row['num']
    ); }
echo json_encode($arr);
mysql_close($conn);
?>

