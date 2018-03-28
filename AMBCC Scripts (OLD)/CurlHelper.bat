@echo off

echo.
echo Executing CurlHelper.bat
echo.

echo cd=%cd%
echo dp0=%~dp0

set gateway="https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=593b9b3a1c763d32832b01aa9345dfcc0721c2d7&version=2016-05-20"
set params=%~dp0\myparams.json

rem set testIm=C:\Users\Andrew Raappana\Desktop\Andrews Magic BCC\AMBCC Scripts\CroppedImageDirectory\test1__1\overlap1--Sample--1--Object--1.jpg

echo.
echo Making Directory %cd%\jsonDat
set jsonDir=%cd%\jsonDat
mkdir "%jsonDir%"

rem rem curl -k -X POST -F "imagesfile=@%testIm%" -F "parameters=@%params%" %gateway% >"%jsonDir%\test--2--2--1--2--1.json"

for /r "%cd%" %%t in (*.jpg) do (


	echo.
	echo.
	echo.
	echo.
	echo.
	echo.
	echo.
	echo.
	echo.
	echo t=%%t
	echo.
	echo params=%params%
	echo.
	echo gateway=%gateway%
	echo.
	echo json=%jsonDir%
	echo.
	echo nt=%%~nt

	pause

	rem putting %%~n infront of a parameter gets things from the parameter! (not variables)	

	curl -k -X POST -F "imagesfile=@%%t" -F "parameters=@%params%" %gateway% >"%jsonDir%\%%~nt.json"


	rem echo %%t
	rem echo %%~nt

)




rem	echo.
rem	echo curl -k -X POST -F "imagesfile=@%%t" -F "parameters=@%params%" %gateway% >"%jsonDir%\%%~nt.json"	
rem	echo.
rem	echo curl BING "imagesfile=@%%t" BING "parameters=@%params%" BING %gateway% BING "%jsonDir%\%%~nt.json"	
rem	echo.
rem	echo BING "imagesfile=@%%t" BING "parameters=@%params%" BING %gateway% BING "%jsonDir%\%%~nt.json"	
rem	echo AYE AYE AYE
rem	echo %jsonDir%\%%~nt.json



