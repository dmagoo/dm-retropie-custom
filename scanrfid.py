#!/usr/bin/python
import time, logging, signal, sys
from subprocess import call
import sysv_ipc
import RPi.GPIO as GPIO

from __init__ import getConfig
from rfid.cardscanner import CardScanner
from rfid.cardserver import CardServer
from emulationstation import EmulationStation
from emulationstation import UserDB

config = getConfig()

logging.basicConfig(
    filename=config.get('logging', 'log_path'),
    level=logging.DEBUG,
    format='%(asctime)s [scanrfid] %(message)s'
)

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
signal.signal(signal.SIGTERM, end_read)

server = CardServer(
    CardScanner(config.getint('rfid','read_delay'), config.getint('rfid', 'scan_delay')),
    sysv_ipc.MessageQueue(config.getint('rfid', 'message_queue_key'), sysv_ipc.IPC_CREAT),
    EmulationStation(config.get('emulationstation', 'runcommand_path')),
    UserDB(config.get('emulationstation', 'db_path'))
)
logging.debug("running service")
server.run()
