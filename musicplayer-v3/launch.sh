#!/bin/sh


AppDir=$(pwd)
AppExecutable="src/main.py"
Arguments=""
PerformanceMode=0

echo --------------------------------------------------------------------
echo ":: APPLYING ADDITIONNAL CONFIGURATION"
echo --------------------------------------------------------------------

#. /mnt/SDCARD/.tmp_update/script/stop_audioserver.sh
if [ "$PerformanceMode" = "1" ]; then echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; fi

cd "$AppDir"

ParasytePath="/mnt/SDCARD/.tmp_update/lib/parasyte"
export PYTHONPATH=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload
export PYTHONHOME=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload
export LD_LIBRARY_PATH=$ParasytePath:$ParasytePath/python2.7/:$ParasytePath/python2.7/lib-dynload:$LD_LIBRARY_PATH


export FFPLAY_PATH=/mnt/SDCARD/.tmp_update/bin/ffplay

echo running "$AppDir/$AppExecutable" ...
touch /tmp/stay_awake
eval /mnt/SDCARD/.tmp_update/bin/parasyte/python2 \"$AppDir/$AppExecutable\" $Arguments > out.txt 2>&1



unset LD_PRELOAD
rm -f /tmp/stay_awake


echo -ne "\n\n" 