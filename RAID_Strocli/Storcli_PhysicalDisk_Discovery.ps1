#author:shizhenning
#----20230921V001----#

$Path_tool =  "C:\Program Files\MegaCli\"
cd $Path_tool

$Count_Physical_Disk =  (.\storcli64.exe /c0  show |findstr "^Physical" | Out-String).Split("=")[-1]      #获取物理磁盘总数量
$PDisk_Discovery = .\storcli64.exe /c0  show J nolog  
$Data_Source = $PDisk_Discovery | ConvertFrom-Json                         #json转换成自定义对象
$Raid_Info = $Data_Source.Controllers[0]  
$Location_Physical_Disk = $Raid_Info.'Response Data'.'PD LIST'.'EID:Slt'   #获取物理磁盘位置,形如32:0,32:1,32:2

### 构造json格式

$VAR1="{"
$VAR2='"data": ['
$VAR3='"{#PDISK}":'
$VAR4="]"
$VAR5="}"
$VAR6="},"

Write-Output $VAR1
Write-Output "   $VAR2"

ForEach($i in $Location_Physical_Disk)
{
Write-Output "      $VAR1"
Write-Output "         $VAR3 `"$i`""
    if ($i -eq $Location_Physical_Disk[-1])
    {         
        Write-Output "      $VAR5"

    }
    else
      {         
        Write-Output "      $VAR6"

    }

}

Write-Output "   $VAR4"
Write-Output $VAR5

