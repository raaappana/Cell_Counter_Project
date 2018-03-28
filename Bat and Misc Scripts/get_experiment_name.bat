rem This bat file is for the purpose of finding a proper experiment name to save as
rem 
rem 
rem
rem
rem
rem
rem
rem

For /F "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate1=%%c-%%a-%%b)

:getExpNameLoop

set "expName="
set /p expName="Save project as:"

if "%expName%"=="" goto Empty

if EXIST "%OutF%\%expName%" (
	echo Experiment name already exists, please choose another name
	echo.
	goto getExpNameLoop
)

goto endExpName

:Empty
set /a fileIter=0

:addone
set /a "fileIter+=1"

if exist "%OutF%\Experiment_%fileIter%_%mydate1%" goto addone

echo.
set /p defaulter="Input empty, save experiment as 'Experiment_%fileIter%_%mydate1%'? (y/n):"

if "%defaulter%"=="" goto Empty

if %defaulter%==n (
echo.
goto getExpNameLoop
)

if %defaulter%==y goto saveExperimentDefault

goto Empty





:saveExperimentDefault

set expName=Experiment_%fileIter%_%mydate1%

:endExpName

echo Making directory "%expName%" in directories "Results" and "Former Inputs"  

mkdir "%OutF%\%expName%"
mkdir "%ArchiveF%\%expName%"


