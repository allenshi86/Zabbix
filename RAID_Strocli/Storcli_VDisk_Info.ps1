#author:shizhenning
#----20230921V001----#

$Path_tool =  "C:\Program Files\MegaCli\"
cd $Path_tool


$No_VDisk = $args[0]  #参数为获取虚拟磁盘名称,形如0/0,1/1
$No_VDisk = $No_VDisk.split("/")[-1]
$Attr_VDisk_Query = $args[1]  #参数选项name,size,type,state,cache,scc等 

$Attr_VDisk = .\storcli64.exe /c0  /v$No_VDisk  show J  NOLOG
$Attr_Source = $Attr_VDisk | ConvertFrom-Json  #获取虚拟磁盘属性列表,比如name,size,type,state,cache,scc等

Write-Output  $Attr_Source.Controllers[0].'Response Data'.'Virtual Drives'.$Attr_VDisk_Query
