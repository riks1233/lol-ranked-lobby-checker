@ECHO:
@echo off
set "currentFilePath=%cd%"
set "venvPath=%currentFilePath%\..\venv"
set "srcPath=%currentFilePath%\..\src"
@REM The following is the incorrect way of setting variables in batch script.
@REM set currentFilePath="%cd%"
@REM set venvPath="%currentFilePath%\..\venv"
@REM set srcPath="%currentFilePath%\..\src"
IF exist %venvPath% (
  call "%venvPath%\Scripts\activate.bat" && python "%srcPath%\main.py" && "%venvPath%\Scripts\deactivate.bat"
) ELSE (
  @ECHO "Python virtual env is missing (`%venvPath%`.) Please read README.md and set up the project, if you haven't done it yet. In case you did, well, then something is broken with the file paths.
)
@PAUSE
