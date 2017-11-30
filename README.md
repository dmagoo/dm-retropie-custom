NOTES For Tweaking RetroPie to work with hardware additions
=======================

#add american sources, default seems to fail
sudo nano /etc/apt/sources.list
# comment out first line, add this:
deb http://mirror.us.leaseweb.net/raspbian/raspbian jessie main contrib non-free rpi

sudo apt-get update
sudo reboot

SETUP MATRIX
===============
https://learn.adafruit.com/neopixels-on-raspberry-pi/software

```bash
sudo apt-get install build-essential
sudo apt-get install git
sudo apt-get install python-dev
sudo apt-get install scons
sudo apt-get install swig
cd
mkdir ~/tmp
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python/
sudo python setup.py install
cd examples/
sudo python strandtest.py
```


SETUP FOR MATRIX HARDWARE
==================
Make sure the following lines exist (and are uncommented) in /boot/config.txt

hdmi_force_hotplug=1
hdmi_force_edid_audio=1

Make sure retropi menu audio is set to auto (at least not 3.5 jack)

When working w/ neopixel lib, make sure brightness setting is low. Lights are ridiculously bright.  Try 8 (out of 255!).  Plenty bright for this

SETUP FOR MATRIX SOFTWARE
=================
sudo apt-get install python-numpy python-scipy


DEV FOR MATRIX HOOKS
===================

https://github.com/RetroPie/RetroPie-Setup/wiki/Runcommand

cd /opt/retropie/configs/all
add hooks in runcommand-onstart.sh and/or runcommand-onend.sh


Setup IPC
=================
mkdir ~/tmp/ipc
cd ~/tmp/ipc
wget http://semanchuk.com/philip/sysv_ipc/sysv_ipc-0.7.0.tar.gz
tar -xvf sysv_ipc-0.7.0.tar.gz
cd sysv_ipc-0.7.0/
sudo python setup.py install


Setup RFID
===============

http://www.instructables.com/id/Raspberry-Pi-3-Model-B-MIFARE-RC522-RFID-Tag-Readi/

```bash
sudo raspi-config
#Use the interactive menu to enable the SPI Interface.
#dtparam=spi=on
#Reboot pi
#verify SPI active:
grep dtparam /boot/config.txt
#make sure dtparam=spi=on is there and not commented out

git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
sudo python setup.py install
cd ..
git clone https://github.com/mxgxw/MFRC522-python.git
cd MFRC522-python
python Read.py

#if it works, move the lib to a global locaiton
mkdir -p /home/pi/.local/lib/python2.7/site-packages
cp MFRC522.py /home/pi/.local/lib/python2.7/site-packages/


```

DEV FOR RFID READER
==================
How to trigger a game from CLI
```
/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ nes /home/pi/RetroPie/roms/nes/Megaman.nes
```

DEV FOR USB AUDIO
==================
lsusb
cat /proc/asound/modules
#output should be
#0 snd_bcm2835
#1 snd_usb_audio
#need to change that
sudo nano /etc/modprobe.d/alsa-base.conf
#add
0 snd_usb_audio
1 snd_bcm2835

sudo nano /etc/asound.conf

ADD:
pcm.card1 {
type hw card 1
}
ctl.card1 {
type hw card 1
}

pcm.!default card1


Installation of custom Retro Pie scripts
#Copy .system file to:
sudo cp /home/pi/RetroPie-Custom/systemd/marquee.service /etc/systemd/system/

#dont do this one, we are likely changing this so it runs under autostart.sh
#sudo cp /home/pi/RetroPie-Custom/systemd/scanrfid.service /etc/systemd/system/

#Edit /opt/retropie/configs/all/autostart.sh so it looks as follows
python /home/pi/RetroPie-Custom/scanrfid.py &
emulationstation #auto


#make sure python executable can be run by pi
chmod +x /home/pi/RetroPie-Custom/scanrfid.py
chmod +x /home/pi/RetroPie-Custom/marqueeserver.py

#enable:
sudo systemctl enable scanrfid.service
sudo systemctl enable marquee.service

sudo systemctl daemon-reload

sudo systemctl start scanrfid.service
sudo systemctl start marquee.service

#move emustation scripts
cp -rf /home/pi/RetroPie-Custom/runcommand/* /opt/retropie/configs/all/
