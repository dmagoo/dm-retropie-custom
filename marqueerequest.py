"""
script to send messages to the marquee-server to queue a display animation
"""
from optparse import OptionParser
import sysv_ipc
from __init__ import getConfig
from display.marqueeserver import MESSAGE_TYPE_MARQUEE
config = getConfig()
mq = sysv_ipc.MessageQueue(config.getint('display', 'message_queue_key'), sysv_ipc.IPC_CREAT)
msg = 'Ping!'

parser = OptionParser()

#message = MarqueeRequest("scrolltext", text="Ping!")
msg = "HA!!!"
mq.send(msg, False, MESSAGE_TYPE_MARQUEE)
#mq.send(message.toJson(), False, MESSAGE_TYPE_MARQUEE)
