param (
    [string]$SourceDirectory,
    [string]$DestinationDirectory
)

# Define source and destination directories
#$sourceDirectory = "C:\Users\97254\Desktop\msc\Thesis\ConvexDrawingDataset\DBPAST2_staged\Puzzle5"
#$destinationDirectory = "D:\msc\for extrapolation 080224"

# Get the last directory name from the source directory
$lastDirectoryName = (Get-Item $sourceDirectory).Name

# Combine the last directory name with the prefix
$prefix = "dbeuropia_" + $lastDirectoryName + "_"

# Get all directories matching the pattern noise_\d
$noiseDirectories = Get-ChildItem -Path $sourceDirectory -Filter "noise_*" -Directory

# Iterate through each noise directory
foreach ($noiseDir in $noiseDirectories) {
    $sourceImagesDirectory = Join-Path -Path $noiseDir.FullName -ChildPath "images"
    
    # Check if the images directory exists in the noise directory
    if (Test-Path -Path $sourceImagesDirectory) {
        # Extract the noise number from the directory name
        $noiseNumber = [regex]::Match($noiseDir.Name, '\d+').Value

        if ($noiseNumber -lt 3)
        {
            # Create destination directory name
            $destinationNoiseDirectory = Join-Path -Path $destinationDirectory -ChildPath ($prefix + "noise_" + $noiseNumber)
        
            # Create destination directory if it doesn't exist
            if (-not (Test-Path -Path $destinationNoiseDirectory)) {
                New-Item -Path $destinationNoiseDirectory -ItemType Directory | Out-Null
            }
        
            # Copy images from source to destination
            Copy-Item -Path $sourceImagesDirectory\* -Destination $destinationNoiseDirectory -Recurse -Force
        }
    }
}
