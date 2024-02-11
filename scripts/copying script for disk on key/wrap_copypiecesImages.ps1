# Define the folder containing directories
$parentDirectory = "C:\Users\97254\Desktop\msc\Thesis\ConvexDrawingDataset\DBeuropia_staged"

# Get a list of directories in the parent directory
$directories = Get-ChildItem -Path $parentDirectory -Directory

# Iterate over each directory
foreach ($directory in $directories) {
    # Construct the source directory path
    $sourceDirectory = $directory.FullName

    # Construct the destination directory path
    $destinationDirectory = "D:\msc\for extrapolation 080224" # "C:\path\to\destination"

    Write-Host $sourceDirectory

    # Run the script for the current directory
    & ".\copypiecesImages.ps1" -SourceDirectory $sourceDirectory -DestinationDirectory $destinationDirectory
}
