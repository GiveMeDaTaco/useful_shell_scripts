# Specify the path to the directory to index
$directoryPath = 'C:\Your\Directory\Path'

# Specify the path to the output .csv file
$outputPath = 'C:\Your\Output\Path\directoryIndex.csv'

# Get all items in the directory and subdirectories
$directoryIndex = Get-ChildItem -Path $directoryPath -Recurse 

# Output the information to the .csv file
$directoryIndex | Select-Object FullName, LastWriteTime, Length | Export-Csv -Path $outputPath -NoTypeInformation

