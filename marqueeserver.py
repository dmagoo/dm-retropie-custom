#!/usr/bin/python
import sys, signal, logging, time
import sysv_ipc

from __init__ import getConfig
from display import Matrix

config = getConfig()

MQ_KEY = config.getint('display', 'message_queue_key')
READ_DELAY = 2

logging.basicConfig(filename=config.get('logging', 'log_path'),
                    level=logging.DEBUG,
                    format='%(asctime)s [marqueeserver] %(message)s'
)

logging.info("starting up")

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    logging.info("CTRL-C detected, shutting down")
    matrix.clearStrip().strip.show()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

logging.info("Matrix Initialization and Test")
matrix = Matrix(32,8)
matrix.test()
logging.info("Matrix Test Complete")
mq = sysv_ipc.MessageQueue(MQ_KEY, sysv_ipc.IPC_CREAT)

continue_polling = True
while continue_polling:
    time.sleep(READ_DELAY)
    try:
        m = mq.receive(False)
        logging.info('message received ' + m[0])
    except sysv_ipc.BusyError:
        pass
