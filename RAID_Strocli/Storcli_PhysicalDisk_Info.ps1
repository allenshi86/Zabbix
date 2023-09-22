#author:shizhenning
#----20230922V002----#

$Path_tool =  "C:\Program Files\MegaCli\"
cd $Path_tool

$Location_Physical_Disk = $args[0]       #参数格式[32:6],即磁盘盘位
$Attr_PDisk = $args[1]                   #参数选项 State, Size ,Interface(SAS\SATA),Model，
       
$DID_Physical_Disk = $Location_Physical_Disk.split(":")[1].Split("]")[0]    #从形如[32:2]格式的盘位获取磁盘ID 2,供storcli /s调用
$Number_Enclousure = $Location_Physical_Disk.split(":")[0].Split("[")[-1]    #获取Enclousure ID,比如32  
$PDAttr_info =.\storcli64.exe /c0  /e$Number_Enclousure /s$DID_Physical_Disk  show J  NOLOG 
$Attr_Source = $PDAttr_info | ConvertFrom-Json                              #获取磁盘属性列表,比如State, Size ,Interface(SAS\SATA),Model等

Write-Output  $Attr_Source.Controllers[0].'Response Data'.'Drive Information'.$Attr_PDisk 
