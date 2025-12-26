param(
    [Parameter(Position=0)]
    [string]$ScriptName
)

# Check if script name was provided
if (-not $ScriptName) {
    Write-Host "Error: Please provide a script name"
    exit 1
}

# Construct the script path using the input
$scriptPath = "solutions\$ScriptName.py"

# Check if the script exists
if (Test-Path $scriptPath) {
    Write-Host "Running $scriptPath..."
    python $scriptPath
} else {
    Write-Host "Error: Could not find $scriptPath"
    exit 1
}