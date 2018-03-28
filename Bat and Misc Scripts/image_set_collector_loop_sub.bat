rem
rem
rem
rem
rem
rem
rem
rem
rem
rem
rem

rem -----------------ONE TIME SET UP-----------------

echo.
echo.
echo Executing image_set_collector_loop_sub.bat
echo.



set i=0





rem -----------------START AND RESTART THE PROGRAM HERE--------------------


:loopNewSet

For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
set fileDirWTime=%SampleSetName%__%mydate%__debugTimeStamp

set outputDir=%expIn%\%fileDirWTime%

echo Making subdirectory "%fileDirWTime%" in %expIn%
echo.
echo --------------------------------------------
mkdir "%outputDir%"



:loop1

set /a i=%i%+1

echo.
echo.
echo Set Name: "%SampleSetName%" :: Sample Number: %i%
echo *==========================================*
echo *    Collect ALL images for this sample    *
echo *==========================================*

echo Making directory "%outputDir%\%i%"
mkdir "%outputDir%\%i%"


:looper1noheader
set "sampleGet="


echo.
set /p sampleGet="Are there more samples in this set? (y/n):" 
if "%sampleGet%" == "" (
	echo Input Invalid. Input 'y' to move on to the next smear or 'n' to move on to the next set of samples.
	goto looper1noheader
)


if %sampleGet% == y goto selectionMade

if %sampleGet% ==n goto selectionMade


echo Invalid Input
goto looper1noheader



:selectionMade


rem PROCESS ALL THE IMAGES IN THIS SAMPLE

echo.
echo *-------------------------------------------------------------------------------------------*


echo.
echo Moving JPG2 files to "%outputDir%\%i%"
cd %WatchedFolderLocation%

rem echo DEBUGGER MODE: COPY INSTEAD OF MOVE
echo DEBUG echo %cd%
rem xcopy *.jp2 "%outputDir%\%i%"
move *.jp2 "%outputDir%\%i%"

cd "%origDir%"

echo.
echo Converting JP2 files to JPG
Call "%batPath%\JP2ToJP.bat"

echo.
echo Moving JPEG2000 files to subfolder "JP2 Dump" in %outputDir%"
cd "%outputDir%\%i%"
mkdir "JP2 Dump"
move *.jp2 "JP2 Dump"
if exist "%cd%/JP2 Dump" (del /q "JP2 Dump")
cd "%origDir%"

echo.
echo *-------------------------------------------------------------------------------------------*
echo.
echo.


ping localhost -n 2 >NULs



rem MOVE ON TO NEXT SET IF YES WAS SELECTED
if %sampleGet%==y (goto loop1)


:end1

set "i="

echo.
echo Exiting image_set_collector_loop_sub.bat
echo.