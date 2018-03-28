rem This bat file is meant to handle most of the higher level processes in the image collection.
rem 
rem The first thing done is setting the watchedfolder.txt text as a variable and then to call im_set_col_loop to collect the images
rem After image_set_collector_loop.bat is finished, the user gets the option of restarting the program- which will result in the program recalling image_set_loop
rem
rem
rem





rem -----------------ONE TIME SET UP-----------------
@echo off

echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo Executing image_collector_main.bat
echo.

rem SET THE WATCHED FOLDER SPECIFIED IN WatchedFolder.txt
FOR /F "tokens=* delims=" %%x IN (WatchedFolder.txt) DO SET WatchedFolderLocationSans=%%x
set WatchedFolderLocation="%WatchedFolderLocationSans%"

echo WatchedFolderLocation=%WatchedFolderLocation%
echo WatchedFolderLocationSans=%WatchedFolderLocationSans%
echo.
echo ------------------------------------------------------------------------------------------------------------------------







rem -----------------START AND RESTART THE PROGRAM HERE--------------------

:programStart

rem INIT RESTARTU (for checking if user wants to restart image collection)
set "restartU="

rem PROCESS IMAGES INPUT INTO THE FOLDER

CALL "%batPath%\image_set_collector_loop.bat"

rem ASK USER IF THEY NEED TO COLLECT MORE SAMPLES
rem echo.
rem set /p restartU="Collect more images? (y/n || default: no):"
rem echo.
rem if %restartU% == y (
rem	goto programStart
rem	)
rem if %restartU% == yes (
rem 	goto programStart
rem	)

echo.
echo Exiting image_collector_main.bat
echo.
echo.