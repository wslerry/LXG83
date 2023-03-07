@echo off
set PYTHONPATH=C:\Python25
path C:\Python25\DLLs;C:\Python25\Scripts;C:\Python25\Lib;C:\Python25;"C:\Program Files (x86)\ArcGIS\bin";%path%

REM ---------------------------------------
REM 			!! ALERT !!
REM 		  !! READ THIS !!
REM         Change parameter here
REM Bulk migrating MDB to GDB
REM mdb_file - Directory of *.MDB files
REM output_folder - New directory for output GDB
REM ---------------------------------------

set "mdb_file=c:/path/to/file.mdb"
set "output_folder=C:\Datasets\Smart_EIS_GIS_202302_GDB"

REM ---------------------------------------


setlocal EnableDelayedExpansion

if exist %mdb_file% (
python mdb2gdb.py "%mdb_file%" %output_folder% "" ""
) else goto :eof

endlocal