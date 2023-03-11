@echo off
set PYTHONPATH=C:\Python25
path C:\Python25\DLLs;C:\Python25\Scripts;C:\Python25\Lib;C:\Python25;"C:\Program Files (x86)\ArcGIS\bin";%path%

REM ---------------------------------------
REM 			!! ALERT !!
REM 		  !! READ THIS !!
REM         Change these parameters
REM sde_connection -> IP address to 8i SDE server. Set it first!
REM output_folder -> Directory to save *.GDB file
REM division -> Query only selected division, eg. KCH
REM lasis_type -> CMS, APIS, EIS, GAZETTE, PLIS, LAAS, LAND, VIS
REM ---------------------------------------

set "sde_connection=10.17.106.208"
set "output_folder=C:\LXG\V2\LXG83\test"
set "gdb_filename=KPT_CMS.gdb"
set "division=KPT"
set "lasis_type=CMS"

REM ---------------------------------------

setlocal EnableDelayedExpansion

set "STARTTIME=%time: =0%"
echo [%STARTTIME%] Migration begin...

python sde2gdb.py %sde_connection% %output_folder% %gdb_filename% %division% %lasis_type%

set "ENDTIME=%time: =0%"
echo [%ENDTIME%] Migration end...

rem Change formatting for the start and end times
for /F "tokens=1-4 delims=:.," %%a in ("%STARTTIME%") do (
	set /A "start=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
)

for /F "tokens=1-4 delims=:.," %%a in ("%ENDTIME%") do ( 
	IF %ENDTIME% GTR %STARTTIME% set /A "end=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100" 
	IF %ENDTIME% LSS %STARTTIME% set /A "end=((((%%a+24)*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100" 
)

rem Calculate the elapsed time by subtracting values
set /A elapsed=end-start

rem Format the results for output
set /A hh=elapsed/(60*60*100), rest=elapsed%%(60*60*100), mm=rest/(60*100), rest%%=60*100, ss=rest/100, cc=rest%%100
if %hh% lss 10 set hh=0%hh%
if %mm% lss 10 set mm=0%mm%
if %ss% lss 10 set ss=0%ss%
if %cc% lss 10 set cc=0%cc%

set DURATION=%hh%:%mm%:%ss%.%cc%

echo Total processing : %DURATION%

goto :eof
endlocal