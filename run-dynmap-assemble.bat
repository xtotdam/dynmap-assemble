@echo off
setlocal enabledelayedexpansion
for /F "tokens=2 delims==" %%a in ('wmic os get localdatetime /value') do set "datetime=%%a"
set "dateandtime=!datetime:~0,4!-!datetime:~4,2!-!datetime:~6,2!_!datetime:~8,2!-!datetime:~10,2!"
echo !dateandtime!
set "theyear=!datetime:~0,4!"
set "themonth=!datetime:~4,2!"
set "thedate=!datetime:~6,2!"
@echo on
mkdir DynmapRenders
mkdir DynmapRenders\Year-%theyear%
mkdir DynmapRenders\Year-%theyear%\Month-%themonth%
mkdir DynmapRenders\Year-%theyear%\Month-%themonth%\Date-%thedate%
python3 dynmap-assemble.py --world world --map t --bgcolor transparent --resize 16 --output DynmapRenders\Year-%theyear%\Month-%themonth%\Date-%thedate%\%dateandtime%.png
endlocal