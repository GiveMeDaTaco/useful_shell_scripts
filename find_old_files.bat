# Specify the path to the directory to search
$directoryPath = 'C:\Your\Directory\Path'

# Specify the path to the output .csv file
$outputPath = 'C:\Your\Output\Path\oldFiles.csv'

# Get the current date
$currentDate = Get-Date

# Subtract 7 years from the current date
$dateLimit = $currentDate.AddYears(-7)

# Get all files in the directory and subdirectories, filter them by LastWriteTime property
$oldFiles = Get-ChildItem -Path $directoryPath -Recurse -File | Where-Object { $_.LastWriteTime -lt $dateLimit }

# Output the full names of the old files and their owners to the .csv file
$oldFiles | ForEach-Object {
    $owner = (Get-Acl -Path $_.FullName).Owner
    [PSCustomObject]@{
        'File Path' = $_.FullName
        'Owner' = $owner
    }
} | Export-Csv -Path $outputPath -NoTypeInformation

