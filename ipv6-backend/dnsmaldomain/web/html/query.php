<?php
#$domain="valework.com.";
#$domain="baidu.com.";
$domain=$_GET["domain"];

$mysql_server_name='deepoceandb';

$mysql_username='zjc';

$mysql_password='zjc13120709021';

$mysql_database='dns';
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting");
mysql_select_db($mysql_database);


$sql = "select * from location where domain = '$domain'";
$result = mysql_query($sql,$conn);
$row = mysql_fetch_array($result);
if ($row[0]){
    $insql = "-1";
}else{
    $insql = "1";
}

//$result=exec("python /home/spark/svm/chaxun.py".' '.$domain);
//$string=explode(",",$result);


$arr[]=array(
'domain' => $domain,
'result' => $insql,
'country'=> $row['country'],
'city' => $row['city'],
'latitude' => $row['latitude'],
'longitude' => $row['longitude']
);

echo json_encode($arr)
?>