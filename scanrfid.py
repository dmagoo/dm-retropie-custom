#!/usr/bin/python
import time, logging, signal, sys
from subprocess import call
import RPi.GPIO as GPIO

from rfid.cardscan import CardScanner
from rfid.cardserver import CardServer

#so we don't keep trying to launch games if the card is left over
#the sensor

logging.basicConfig(filename='/tmp/retropie-custom.log',level=logging.DEBUG,format='%(asctime)s [scanrfid] %(message)s')

#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    logging.info("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    sys.exit()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
logging.debug("there")
server = CardServer(CardScanner())
logging.debug("here")
server.run()
