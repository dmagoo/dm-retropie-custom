#!/usr/bin/python
import sys, signal, logging
import sysv_ipc

from __init__ import getConfig
from display import Matrix
from display import MarqueeServer

config = getConfig()

MQ_KEY = config.getint('message_queue', 'key')

logging.basicConfig(filename=config.get('logging', 'log_path'),
                    level=logging.DEBUG,
                    format='%(asctime)s [marqueeserver] %(message)s'
)

logging.info("starting up")

# Capture SIGINT for cleanup when the script is aborted via ctlr-c
# and sigterm when aborted by systemd
def end_read(signal,frame):
    logging.info("CTRL-C detected, shutting down")
    matrix.clearStrip().strip.show()
    sys.exit()

signal.signal(signal.SIGINT, end_read)
signal.signal(signal.SIGTERM, end_read)

logging.info("Matrix Initialization and Test")
matrix = Matrix(32,8)
matrix.strip.begin()
#matrix.test()
logging.info("Matrix Test Complete")

logging.info("Starting marquee server")
server = MarqueeServer(
    matrix,
    sysv_ipc.MessageQueue(MQ_KEY, sysv_ipc.IPC_CREAT)
)

server.run()
