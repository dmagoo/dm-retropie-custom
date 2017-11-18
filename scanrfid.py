#!/usr/bin/python
import time
from subprocess import call
import RPi.GPIO as GPIO
import MFRC522
import signal
import sys

#so we don't keep trying to launch games
SCAN_DELAY = 10

MODE_LAUNCH = 0
MODE_REGISTER = 1
GPIO.cleanup()

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    sys.exit()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Scanning for RFID Tags"

cmd = "/opt/retropie/supplementary/runcommand/runcommand.sh"

registered_games = {"62,170,161,185" : ["0", "_SYS_", "nes", "/home/pi/RetroPie/roms/nes/Megaman.nes"]}

#mode = MODE_LAUNCH
mode = MODE_REGISTER

def poll_for_scan():
    continue_reading = True
    while continue_reading:
        
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"
        
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            # Print UID
            uid = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
            print "Card read UID: " + uid

            if MODE_LAUNCH == mode:
                if(registered_games.get(uid)):
                    yield registered_games.get(uid)
                    time.sleep(SCAN_DELAY)

            elif MODE_REGISTER == mode:
                yield None
                pass
                
for game in poll_for_scan():
    if MODE_LAUNCH == mode:
        print game
        call([cmd] + game)
    else:
        print "Card Found"
        sys.exit(0)
