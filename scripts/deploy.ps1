# Local Windows PowerShell; run from repository root.
# Copies files only. Does NOT flash Arduino firmware or start motors.
$ErrorActionPreference = "Stop"
$destination = "mayok1921@192.168.7.2:/home/mayok1921/robotic_arm"
Write-Host "Sending experimental modular controller to Orange Pi..." 
ssh mayok1921@192.168.7.2 "mkdir -p ~/robotic_arm/src ~/robotic_arm/config"
if ($LASTEXITCODE -ne 0) { throw "Remote directory creation failed" }
scp .\src\*.py "${destination}/src/"
if ($LASTEXITCODE -ne 0) { throw "Python transfer failed" }
scp .\config\settings.json "${destination}/config/settings.json"
if ($LASTEXITCODE -ne 0) { throw "Config transfer failed" }
Write-Host "Files copied. NOT started. v2 firmware must be flashed independently before running python3 -m src.control."
