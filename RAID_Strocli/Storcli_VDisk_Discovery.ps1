#author:shizhenning
#----20231009V003----#

$Path_tool =  "C:\Program Files\MegaCli\"
cd $Path_tool

$Count_Physical_Disk =  (.\storcli64.exe /c0  show |findstr "^Virtual" | Out-String).Split("=")[-1]      #获取虚拟磁盘总数量
$VDisk_Discovery =  .\storcli64.exe /c0  show J nolog 
$Data_Source = $VDisk_Discovery | ConvertFrom-Json  #json转换成复的自定义对象
$Raid_Info = $Data_Source.Controllers[0]  
$Number_VDisk = $Raid_Info.'Response Data'.'VD LIST'.'DG/VD' #获取虚拟磁盘名称,形如0/0,1/1

### 构造json格式

$VAR1="{"
$VAR2='"data": ['
$VAR3='"{#VDISK}":'
$VAR4="]"
$VAR5="}"
$VAR6="},"

Write-Output $VAR1
Write-Output "   $VAR2"

if ($Number_VDisk -is "System.Array") {
   ForEach($i in $Number_VDisk){
     Write-Output "      $VAR1"
     Write-Output "         $VAR3 `"$i`""
       if ($i -eq $Number_VDisk[-1])
       {         
          Write-Output "      $VAR5"
       }
       else
       {         
          Write-Output "      $VAR6"
       }
  }
}
else 
{
     Write-Output "      $VAR1"
     Write-Output "         $VAR3 `"$Number_VDisk`""
     Write-Output "      $VAR5"
 }


Write-Output "   $VAR4"
Write-Output $VAR5

