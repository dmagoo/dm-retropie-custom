#!/usr/bin/env bash

system="$1"
emulator="$2"
rom_path="$3"
cmd="$4"

#check if service is active, so we can return to it's state after
#restart_service=`systemctl -q is-active scanrfid.service && echo YES || echo NO`

#if [[ "YES" = $restart_service ]];
#then
#    echo "stopping card reader service"
#    sudo systemctl stop scanrfid.service
#fi

echo "waiting for scan (or cancellation)"

dialog --title "Scan Item" --msgbox 'Hold RFID item close to sensor' 6 20

#dpid=$!
clear
#python /home/pi/RetroPie-Custom/scanrfid.py register
#fire up a script that will send a register-mode request to the rfid reader daemon
#any card scanned at this time will be bound to this rom / emulator
python /home/pi/RetroPie-Custom/rfidregister.py -r $rom_path -s $system -e $emulator
#ret=$?
#if [ $ret -ne 0 ]; then
#    echo "fail"
#else
#    echo "good"
#fi
#kill $dpid

#if [[ "YES" = $restart_service ]];
#then
#    echo "restarting card reader service"
#    sudo systemctl start scanrfid.service
#fi
#dialog --title "Scan Item" --msgbox 'Item registered' 6 20

echo $@ > /tmp/rcmenu.log

