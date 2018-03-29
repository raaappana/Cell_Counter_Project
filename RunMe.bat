@echo off
set BatDir="%~dp0\batFiles"
set origDir="%~dp0"

echo Executing RunMe.bat
echo.

echo *===================================================*
echo * DO NOT USE SPECIAL CHARACTERS OR SPACES IN INPUTS *
echo *===================================================*
echo.

FOR /F "tokens=* delims=" %%x IN (WatchedFolder.txt) DO SET WatchedFolderLocationSans=%%x
set WatchedFolderLocation="%WatchedFolderLocationSans%"

:: Look at what our WatchedFolder is
set Watched

echo.
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo.

:programStart

CALL GetSampleSetNameAndInitSmears.bat

set "restartU="

echo.
set /p restartU="Restart Program? (y/n || default: no):"
echo.

if %restartU% == y (goto programStart)
if %restartU% == yes (goto programStart)

echo.
echo Closing Program.

rem PING localhost -n 6 >NUL
