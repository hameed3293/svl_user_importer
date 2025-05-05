# Define paths
$lambdaDir = "lambda"
$buildDir = "build"

# Clean previous build
if (Test-Path $buildDir) {
    Remove-Item $buildDir -Recurse -Force
}
New-Item -ItemType Directory -Path $buildDir | Out-Null

# Install dependencies
pip install -r "$lambdaDir\requirements.txt" -t $buildDir

# Copy handler code
Copy-Item "$lambdaDir\handler.py" "$buildDir\"

# Run Pulumi with new build
pulumi up