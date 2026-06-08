<#
.SYNOPSIS
    Gathers core system cpu and ram metrics.
.DESCRIPTION
    Reads windows performance metrics
#>

$Ram = Get-CimInstance Win32_OperatingSystem

#Package and output everything directly as a compressed JSON string
[PSCustomObject]@{
    pc_name       = $env:COMPUTERNAME
    os_type       = "Windows"
    cpu_usage_pct = [int](Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
    total_ram_gb  = [math]::Round($Ram.TotalVisibleMemorySize / 1024 / 1024, 2)
    free_ram_gb   = [math]::Round($Ram.FreePhysicalMemory / 1024 / 1024, 2)
} | ConvertTo-Json -Compress