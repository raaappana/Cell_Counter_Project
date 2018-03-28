@echo off

rem This is the executed part of my program.
rem The code initially attempts to set a few globally used variables


rem *==============================================================================*
rem I should sort through every jpg file in a folder and then rename it to order it by time.
rem *==============================================================================*




echo *==============================================================================*
echo *                                                                              *
echo *       *-_-'-_-* RUNNING ANDREW'S MAGIC BLOOD CELL COUNTER *-_-'-_-*          *
echo *                          Made by: Andrew Raappana                            *
echo *                                  v0.02                                       *
echo *==============================================================================*
echo.
echo NOTE: This program is unstable. Expect errors.
echo.
echo Thank you,
echo Andrew
echo.
echo.
echo.





set OrigDir=%~dp0
set batPath=%~dp0Bat and Misc Scripts
set AMBCC=%~dp0AMBCC Scripts
set CP=%~dp0CellProfiler3\CellProfiler.exe
set ArchiveF=%~dp0Former Inputs
set OutF=%~dp0Results

set anac3="%~dp0\Anaconda3\python.exe"
set pipe="%~dp0CPpipev05.cppipe"
set tIn="C:\Users\Andrew Raappana\Desktop\Andrews Magic Blood Cell Counter\test"
set tIn2 = %~dp0\Former Inputs\fab1vsbat2


rem "%CP%" -c -r -p %pipe% -i %tIn% -o "%~dp0testOut"

echo *=======================================================*
echo * DO NOT USE SPECIAL CHARACTERS OR SPACES IN ANY INPUTS *
echo *=======================================================*
echo.

call "%batPath%\get_experiment_name.bat"

set expIn=%ArchiveF%\%expName%
echo %expIn%
set expOut=%OutF%\%expName%

call "%batPath%\image_collector_main.bat"








rem --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


echo *=======================================================*
echo *=======================================================*
echo *=======================================================*
echo *              DO NOT EXIT COMMAND PROMPT               *
echo *=======================================================*
echo *=======================================================*
echo *=======================================================*
echo.

echo Calling Cell Profiler to process experiment images

rem Loop through all the set folders in the experiment ---> then loop through all the sample folders in the experiment. Running Cell profiler on each one and then standardizing and moving the
rem resultant db file to to the output folder.

cd %expIn%
for /d %%y in (*) do (
	
	cd %%y
	for /d %%u in (*) do (
		
		cd %%u
		
		echo.
		echo.
		echo Target Dir = %cd%\%%y\%%u
		echo.
	
		"%CP%" -c -r -p %pipe% -i "%cd%\%%y\%%u" -o "%cd%\%%y\%%u"

		rename "%cd%\%%y\%%u\BloodCellObjects.db" %%y__%%u.db
		echo Moving %%y__%%u.db to %expOut%
		move "%cd%\%%y\%%u\%%y__%%u.db" "%expOut%"
		cd ..

	)
	cd ..
)





rem ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

:getAccurateLoop

cd "%expOut%"


echo.
rem TEST READ OF SQL FILES, FIND OUT HOW MANY OBJECTS ARE IN EACH IMAGE.

%anac3% "%AMBCC%\SQLProcessor.py" %*

echo.
set /p accurate=Do these numbers seem accurate?

if "%accurate%" == "" goto getAccurateLoop

if %accurate% == y (
	goto Continue
)

if %accurate% == n (
	goto notAccurate
)

goto getAccurateLoop



:notAccurate

echo Sorry about that. Please consider sending me (Andrew) the images at raappanaa@comcast.net so I can further train the program. 
echo.
echo Close the program now or press enter twice to continue with image analysis.
pause
pause

:Continue

rem ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
echo.
echo Calling Andrew's Magic Blood Cell Counter, target SQLight: TARGET
echo.
echo *=======================================================*
echo *=======================================================*
echo *=======================================================*
echo *              DO NOT EXIT COMMAND PROMPT               *
echo *=======================================================*
echo *=======================================================*
echo *=======================================================*
echo.


%anac3% "%AMBCC%\main.py" %*

xcopy *.xlsx Image-Analysis-Results

:TrueEnd

echo.
echo.
echo --Exiting Andrew's Magic Blood Cell Counter--

PAUSE
