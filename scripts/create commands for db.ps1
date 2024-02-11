# Define the DB parameter value
$DBParameter = "PAST4_excluded"


# Get the list of directories in the specified path
$directories = Get-ChildItem -Directory

# Loop through each directory
foreach ($directory in $directories) {
    # Check if the directory name already starts with "Puzzle"
    if (-not ($directory.Name -match "^Puzzle")) {
        # Rename the directory with the prefix "Puzzle"
        $newName = "Puzzle" + $directory.Name
        Rename-Item -Path $directory.FullName -NewName $newName -Force
    }
}

# Get the list of directories in the current working directory
$directories = Get-ChildItem -Directory

# Loop through each directory
foreach ($directory in $directories) {
    

    # Get the subdirectories within the current directory
    $subDirectories = Get-ChildItem -Path $directory.FullName -Directory

    # Loop through each subdirectory
    foreach ($subDirectory in $subDirectories) {
        # Check if the subdirectory name matches the noise pattern
        if ($subDirectory.Name -match "noise_\d+") {
            # Extract the puzzle number and noise level from the subdirectory name
            $puzzleNum = $directory.Name

            $puzzleNumDisplay = $puzzleNum -replace "^Puzzle", ""

            $noiseLevel = $subDirectory.Name

            $noiseLevelDisplay = $noiseLevel -replace "^noise_",""


            # Construct the command to execute
            $command = "python scripts\puzzle_solution_to_physics.py --DB $DBParameter --puzzle_num $puzzleNumDisplay --noise_level $noiseLevelDisplay --is_stage --is_no_erased_pieces_by_noise"

            # Print the command
            #Write-Host "Command for directory $($subDirectory.FullName):"
            Write-Host $command
            # Invoke-Expression $command  # Uncomment this line to execute the command
        }
    }
}
