@echo off
set PYTHONPATH=C:\Python25
path C:\Python25\DLLs;C:\Python25\Scripts;C:\Python25\Lib;C:\Python25;"C:\Program Files (x86)\ArcGIS\bin";%path%

REM ---------------------------------------
REM 			!! ALERT !!
REM 		  !! READ THIS !!
REM         Change these parameters
REM mdbDir -> Directory of *.MDB files
REM output_folder -> New directory for output GDB
REM ---------------------------------------

set "mdbDir=C:\Datasets\SMARTE~1"
set "output_folder=C:\Datasets\Smart_EIS_GIS_202302_GDB"

REM ---------------------------------------


setlocal EnableDelayedExpansion

for /f "tokens=*" %%i in ('dir /s /b /a-d %mdbDir%\*.mdb') do (
	start /affinity 1F python mdb2gdb.py "%%~i" %output_folder% "" ""
)

goto :eof

endlocal