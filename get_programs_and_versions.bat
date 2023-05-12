# Get installed software information from 32-bit and 64-bit registries
$installedSoftware = (
    # Fetch from 64-bit registry
    Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | 
    Where-Object { 
        ($_.DisplayName -and $_.DisplayVersion) -and ($_.DisplayName -notmatch "\.NET|Cisco") 
    } | 
    Select-Object DisplayName, DisplayVersion
) + (
    # Fetch from 32-bit registry
    Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | 
    Where-Object { 
        ($_.DisplayName -and $_.DisplayVersion) -and ($_.DisplayName -notmatch "\.NET|Cisco") 
    } | 
    Select-Object DisplayName, DisplayVersion
)

# Sort by software name and export to CSV
$installedSoftware | 
Sort-Object DisplayName | 
Export-Csv -Path "InstalledSoftware.csv" -NoTypeInformation -Encoding UTF8

