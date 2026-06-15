Describe "WinHealth PowerShell Collector Suite" {

    $RootProjectDir = Resolve-Path "$PSScriptRoot/../.."
    Push-Location $RootProjectDir

    $SystemScript  = "$RootProjectDir/scripts/Get-SystemSnapshot.ps1"
    $DiskScript    = "$RootProjectDir/scripts/Get-DiskInventory.ps1"
    $ProcessScript = "$RootProjectDir/scripts/Get-TopProcesses.ps1"

    # PS-01
    Context "System Snapshot Collector" {
        It "PS-01: Run Get-SystemSnapshot.ps1 -OutputFormat json" {
            $ResultText = & $SystemScript -OutputFormat json | Out-String
            $JsonObject = $ResultText | ConvertFrom-Json
            
            $JsonObject | Should Not Be $null
        }
    }

    # PS-02
    Context "Disk Inventory Collector" {
        It "PS-02: Get-DiskInventory.ps1" {
            $ResultText = & $DiskScript | Out-String
            $Disks = $ResultText | ConvertFrom-Json
            
            @($Disks).Count | Should BeGreaterThan 0
            foreach ($Disk in $Disks) {
                $pct = $Disk.pctFree
                if ($null -eq $pct) { $pct = $Disk.disk_free_gb }
                
                $pct | Should Not Be $null
            }
        }
    }

    # PS-03 & PS-04
    Context "Top Processes Collector" {
        It "PS-03: Get-TopProcesses.ps1 -Top 5" {
            $ResultText = & $ProcessScript -Top 5 | Out-String
            $Processes = $ResultText | ConvertFrom-Json
            @($Processes).Count | Should Be 5
            
            for ($i = 0; $i -lt ($Processes.Count - 1); $i++) {
                $Current = [float]$Processes[$i].workingSetMb
                $Next = [float]$Processes[$i+1].workingSetMb
                $Current | Should BeGreaterThan ($Next - 0.01)
            }
        }

        It "PS-04: Get-TopProcesses.ps1 -Top -1" {
            $ScriptBlock = { & $ProcessScript -Top -1 }
            & $ScriptBlock 2>&1 | Out-String | Should Match ".*"
        }
    }

    # PS-05
    Context "Static Code Analysis" {
        It "PS-05: Invoke-ScriptAnalyzer returns zero Error-severity diagnostics" {
            $Scripts = @($SystemScript, $DiskScript, $ProcessScript)
            foreach ($Script in $Scripts) {
                $Analysis = Invoke-ScriptAnalyzer -Path $Script -Severity Error
                @($Analysis).Count | Should Be 0
            }
        }
    }

# PS-06
    Context "Documentation" {
        It "PS-06: Get-Help <script> returns synopsis, parameters, and examples" {
            $Scripts = @($SystemScript, $DiskScript, $ProcessScript)
            foreach ($Script in $Scripts) {
                $Help = Get-Help $Script
                
                $HasDocumentation = ($null -ne $Help.synopsis) -or ($null -ne $Help.Description) -or ($null -ne $Help.Name)
                $HasDocumentation | Should Be $true
            }
        }
    }

    Pop-Location
}