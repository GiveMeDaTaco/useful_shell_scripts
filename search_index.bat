# Specify the path to the .csv file
$csvPath = 'C:\Your\Output\Path\directoryIndex.csv'

# Read the .csv file
$directoryIndex = Import-Csv -Path $csvPath

# Prompt the user for a string
$searchString = Read-Host -Prompt 'Input a string to search for'

# Search the index for directories containing the string
$matchingDirectories = $directoryIndex | Where-Object { $_.FullName -like "*$searchString*" -and $_.Length -eq $null }

# Print the matching directories
$matchingDirectories | ForEach-Object { Write-Output $_.FullName }

