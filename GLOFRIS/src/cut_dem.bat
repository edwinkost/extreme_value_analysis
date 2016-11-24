@echo off
REM Batch file to cut a DEM from a large scale DEM
REM
SET LOGFILE=cut_dem.log

echo "Starting cut_dem.bat"  > %LOGFILE%


IF %1nul == nul GOTO usage
IF %2nul == nul GOTO usage
IF %3nul == nul GOTO usage
IF %4nul == nul GOTO usage
IF %5nul == nul GOTO usage
IF %6nul == nul GOTO usage


echo "xmin      [%1]"  >> %LOGFILE%
echo "ymin      [%2]"  >> %LOGFILE%
echo "xmax      [%3]"  >> %LOGFILE%
echo "ymax      [%4]"  >> %LOGFILE%
echo "src_dem   [%5]"  >> %LOGFILE%
echo "dst_dem   [%6]"  >> %LOGFILE%

SET xmin=%1
SET ymin=%2
SET xmax=%3
SET ymax=%4
SET src_dem=%5
SET dst_dem=%6

gdalwarp -te %xmin% %ymin% %xmax% %ymax% %src_dem% temp.tif >> %LOGFILE%
gdal_translate -ot Float32 -of PCRaster temp.tif temp.map >> %LOGFILE%
pcrcalc temp2.map = if(temp.map ge 32768, temp.map-65536,temp.map) >> %LOGFILE%
pcrcalc %dst_dem% = if(temp2.map ne -9999, temp2.map) >> %LOGFILE%

del temp*.*
GOTO end
:usage
echo "USAGE cut_dem <xmin> <ymin> <xmax> <ymax> <source dem> <destination dem>" >> %LOGFILE%
echo "USAGE cut_dem <xmin> <ymin> <xmax> <ymax> <source dem> <destination dem>"
:end


