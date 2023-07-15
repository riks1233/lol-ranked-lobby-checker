
$venvPath = "$PSScriptRoot\..\venv"
$srcPath = "$PSScriptRoot\..\src"
if (Test-Path -Path $venvPath) {
  & $venvPath\Scripts\activate.ps1; python $srcPath\main.py
} else {
  echo "Python virtual env is missing ($venvPath). Please read README.md and set up the project, if you haven't done it yet. In case you did, well, then something is broken with the file paths."
}
Read-Host -Prompt "Press any key to continue"
