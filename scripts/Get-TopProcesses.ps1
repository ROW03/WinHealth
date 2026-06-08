<#
.SYNOPSIS
    Gathers the top memory-consuming processes.
.DESCRIPTION
    Lists the top running processes sorted by Working Set memory size.
#>
Get-Process |
    Sort-Object -Property WS -Descending |
    Select-Object -First 5 |
    Select-Object -Property Id, ProcessName, @{Name='MemoryMB'; Expression={[math]::Round($_.WS / 1024 / 1024, 2)}} |
    ConvertTo-Json