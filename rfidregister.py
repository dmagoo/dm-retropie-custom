"""
script to send messages to the card-server to register an rfid component
"""
import sysv_ipc
from __init__ import getConfig
from rfid.cardserver import MESSAGE_TYPE_REGISTER
config = getConfig()
mq = sysv_ipc.MessageQueue(config.getint('rfid', 'message_queue_key'), sysv_ipc.IPC_CREAT)
mq.send('10', False, MESSAGE_TYPE_REGISTER)
