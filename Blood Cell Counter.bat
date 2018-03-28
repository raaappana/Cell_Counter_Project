@echo off

:: This is the executed file for the program. It acts as the hub that interacts with the python code and cell profiler.
::
:: This program assumes that a microscope is actively inputing images (of JP2 format) into a folder that is monitored by this program. (WatchedFlder.txt contains the path to that folder, so modify that)
:: The user specifies the experiment name, the sample set name, and then starts taking pictures until they are done with a slide from that sample set.
:: After all images from the blood slide are taken, the program asks if there's another sample from the set. If so, they then move onto the next sample.
:: When the user has collected all the images, for their samples, for that particular set, they can move onto the next set.
:: 
:: During this time, the program designs a tree of directories so it that it can call CellProfiler onto all of the images of a particular sample set. 
::
:: When CellProfiler is called it generates n-number of SQLight files, where n is the number of sample sets.
::
:: Following this, I call Python scripts to send cropped cell-images to the WATSON image detection API. 
:: The cell-images are found by the outputted SQLight files, which list the image path and the x,y coordinates of each detected cell.
:: 
:: WATSON then returns a JSON file that lists the probability of the image being an "infected blood cell" or an "uninfected red blood cell"
:: The python scripts (messily) handle the JSON file (messily) and write it into an excel file.

:: --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:: Setting variables containing the paths that are commonly used by the program


:: Setting script, folders, and Cell Profiler paths

set OrigDir=%~dp0
set batPath=%~dp0Bat and Misc Scripts
set AMBCC=%~dp0AMBCC Scripts
set ArchiveF=%~dp0Former Inputs
set OutF=%~dp0Results

:: Setting paths to Cell profiler, the Cell Profiler pipeline, and python (version 3.7) 

set anac3="%~dp0\Anaconda3\python.exe"
set CP=%~dp0CellProfiler3\CellProfiler.exe
set pipe="%~dp0CPpipev05.cppipe"

:: Setting paths to test image files

set tIn="C:\Users\Andrew Raappana\Desktop\Andrews Magic Blood Cell Counter\test"
set tIn2 = %~dp0\Former Inputs\fab1vsbat2

:: FIX IN FUTURE: In case someone reruns the program, remove any pre-established temporary paths in the environment (haven't run into this issue yet though)
:: "%CP%" -c -r -p %pipe% -i %tIn% -o "%~dp0testOut"


:: --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:: Display the logo, and find out the experiment name-make a file in the results folder with the experiment name.
:: Also collect the sample sets, making a file in the exp. folder
:: Then cycle through the collection of images for a sample within that sample set, putting the jpg files into the sample set directory.

:: Logo and notes

echo *==============================================================================*
echo *                                                                              *
echo *                 RUNNING ANDREW'S MAGIC BLOOD CELL COUNTER                    *
echo *                          Made by: Andrew Raappana                            *
echo *                                  v0.02                                       *
echo *==============================================================================*
echo.
echo NOTE: This program might have errors depending on the operating system. It's only been tested on Windows 10
echo.
echo Thank you,
echo Andrew
echo.
echo.
echo.
echo *=======================================================*
echo * DO NOT USE SPECIAL CHARACTERS OR SPACES IN ANY INPUTS *
echo *=======================================================*
echo.

:: Get the experiment name and make an experiment folder in the results folder
call "%batPath%\get_experiment_name.bat"

:: Make a variable 
set expIn=%ArchiveF%\%expName%
echo %expIn%
set expOut=%OutF%\%expName%

call "%batPath%\image_collector_main.bat"








:: --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:: Calling CellProfiler to analyze all the images and produce SQLight files that contain the paths of the images and the x,y coordinates of the detected cells.
:: 

echo *=======================================================*
echo *=======================================================*
echo *=======================================================*
echo *              DO NOT EXIT COMMAND PROMPT               *
echo *=======================================================*
echo *=======================================================*
echo *=======================================================*
echo.

echo Calling Cell Profiler to process experiment images

:: Loop through all the set folders in the experiment ---> then loop through all the sample folders in the experiment. Running Cell profiler on each one and then standardizing and moving the
:: resultant db file to to the output folder.

:: This loop is TERRIBLE. But it does the job well.

cd %expIn%
for /d %%y in (*) do (
	
	cd %%y
	for /d %%u in (*) do (
		
		cd %%u
		
		echo.
		echo.
		echo Target Dir = %cd%\%%y\%%u
		echo.
		
		:: Calls Cell Profiler on all the out 
		"%CP%" -c -r -p %pipe% -i "%cd%\%%y\%%u" -o "%cd%\%%y\%%u"

		rename "%cd%\%%y\%%u\BloodCellObjects.db" %%y__%%u.db
		echo Moving %%y__%%u.db to %expOut%
		move "%cd%\%%y\%%u\%%y__%%u.db" "%expOut%"
		cd ..

	)
	cd ..
)





:: ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:: To ensure that the user doesn't waste money on inaccurate reads (the super computer charges 2 cents per image analyzed),
:: we count the number of cells and ask the user if that's the right amount.

:getAccurateLoop


:: Call the python file SQLProcessor.py to read the SQL files and determine how many cell objects were found.

echo.
cd "%expOut%"
%anac3% "%AMBCC%\SQLProcessor.py" %*


:: Ask the user if the cell numbers seem accurate. If so, continue- if not, ask the user to send them for training the program.

echo.
set /p accurate=Do these numbers seem accurate?

if "%accurate%" == "" goto getAccurateLoop
if %accurate% == y (
	goto Continue
)
if %accurate% == n (
	goto notAccurate
)

::Loop back if they didn't respond right.
goto getAccurateLoop



:: If Cell Profiler goofed, asked for images to get it trained more.
:notAccurate

echo Sorry about that. Please consider sending me (Andrew) the images at raappanaa@comcast.net so I can further train the program. 
echo.
echo Close the program now or press enter twice to continue with image analysis.
pause
pause




:Continue

:: ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:: Call the python scripts that send the images to WATSON and make the excel file. Move that excel file to the top of the experiment folder in the results folder

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

:: Move the python generated excel file (located in the python file location.) to the experiements results folder
xcopy *.xlsx Image-Analysis-Results



:: ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:: Annnnd we're done!

:TrueEnd

echo.
echo.
echo --Exiting Andrew's Magic Blood Cell Counter--

:: Pause for the users, users love to have pauses so they can control the command prompt's departure.
PAUSE
