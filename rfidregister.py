"""
script to send messages to the card-server to register an rfid component
"""
from optparse import OptionParser
import sysv_ipc
import json
from __init__ import getConfig
from messages import MESSAGE_TYPE_REGISTER
config = getConfig()
mq = sysv_ipc.MessageQueue(config.getint('message_queue','key'), sysv_ipc.IPC_CREAT)

parser = OptionParser(usage="usage: %prog [options] rom system")

parser.add_option("-e", "--emulator", dest="emulator",
                                    help="emulator to register, overides system default", metavar="EMULATOR")


(options, args) = parser.parse_args()

if len(args) != 2:
            parser.error("wrong number of arguments, rom and system required")

rom = args[0]
system = args[1]
emulator = options.emulator

msg = {'rom': rom, 'system': system, 'emulator': emulator}

mq.send( json.dumps(msg), False, MESSAGE_TYPE_REGISTER)
