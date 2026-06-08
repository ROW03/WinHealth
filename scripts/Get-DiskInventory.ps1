<#
.SYNOPSIS
    Gathers primary storage disk metrics
.DESCRIPTION
    Looks at the c drive capacity and outputs free space data as JSON
#>
# Grab the hardware properties of the c drive
$Disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"

#mConvert leftover space to gigabytes and output as compressed JSON
[PSCustomObject]@{
    disk_free_gb = [math]::Round($Disk.FreeSpace / 1024 / 1024 / 1024, 2)
} | ConvertTo-Json -Compress