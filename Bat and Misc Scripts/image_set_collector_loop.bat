rem This bat file is
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
echo Executing image_set_collector_loop.bat
echo.











rem -----------------START AND RESTART THE PROGRAM HERE--------------------

:loop2

rem GET SAMPLE SET NAME FROM USER
set "SampleSetName="
set /p SampleSetName="Please input your sample set's name:" 
if "%SampleSetName%" == "" goto loop2

echo.
echo Gathering input samples for sample set "%SampleSetName%"
echo.
echo ------------------------------------------------------------------------------------------------------------------------

CALL "%batPath%\image_set_collector_loop_sub.bat





rem FIND OUT IF THE USER HAS MORE SAMPLE SETS

:check1

set "Continue="

set /p Continue="Are there more sample sets? (y/n): " 
echo.

if "%Continue%" == "" (
	echo Input Invalid. Input 'y' to move on to the next sample set or 'n' to end the program
	goto check1
	)

if %Continue% == y (
	echo.
	echo *===========================================================*
	echo *                                                           *
	echo *                        Next Set                           *
	echo *                                                           *
	echo *===========================================================*
	echo.
	goto loop2
	)

if %Continue% == n (goto end) else (
	echo Input Invalid. Input 'y' to move on to the next sample set or 'n' to end the program
	goto check1
	)




:end

echo Exiting image_set_collector_loop.bat
