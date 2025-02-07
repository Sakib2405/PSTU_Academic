# Define file locations
$fileLocations = @(
    "C:\Users\YourUsername\Documents\academic",
    "H:\My Drive\PSTU_Academic",
    "C:\Users\YourUsername\Desktop\code\problem-solving",
    "C:\Users\YourUsername\Desktop\code\practice-contest",
    "C:\Users\YourUsername\Desktop\gits\logs",
    "C:\Users\YourUsername\Desktop\gits\notes",
    "C:\Users\YourUsername\Desktop\gits\stash-contents"
)

# Function to perform auto push
function AutoPush {
    $currentTime = Get-Date -Format "HH:mm:ss"
    Write-Output "Auto push at $currentTime"
    
    foreach ($fileLocation in $fileLocations) {
        Set-Location $fileLocation
        git add .
        git commit -am "Auto push at $currentTime"
        git pull --rebase
        git push
    }
    
    # Display notification
    [System.Windows.Forms.MessageBox]::Show("Auto push done at $currentTime", "Automation")
}

# Schedule the task to run once per day
while ($true) {
    AutoPush
    Start-Sleep -Seconds 86400  # Sleep for 24 hours
}
