#!/usr/bin/env bash
#check if service is active, so we can return to it's state after
restart_service=`systemctl -q is-active scanrfid.service && echo YES || echo NO`

if [[ "YES" = $restart_service ]];
then
    echo "stopping card reader service"
    sudo systemctl stop scanrfid.service
fi

echo "waiting for scan (or cancellation)"

dialog --title "Scan Item" --msgbox 'Hold RFID item close to sensor' 6 20

#dpid=$!
clear
python /home/pi/RetroPie-Custom/scanrfid.py register
ret=$?
if [ $ret -ne 0 ]; then
    echo "fail"
else
    echo "good"
fi
#kill $dpid

if [[ "YES" = $restart_service ]];
then
    echo "restarting card reader service"
    sudo systemctl start scanrfid.service
fi

dialog --title "Scan Item" --msgbox 'Item registered' 6 20

echo $@ > /tmp/rcmenu.log

