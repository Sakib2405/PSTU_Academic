$env:VIRTUAL_ENV = (Resolve-Path "$PSScriptRoot\..").Path
$env:PATH = "$PSScriptRoot;" + $env:PATH
if ($env:PROMPT -notlike "*(.venv)*") { $env:PROMPT = "(.venv) " + $env:PROMPT }
Write-Output "(.venv) activated"