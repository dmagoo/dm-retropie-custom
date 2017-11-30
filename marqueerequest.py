"""
script to send messages to the marquee-server to queue a display animation
"""
from optparse import OptionParser
import sysv_ipc
from __init__ import getConfig
from messages import MESSAGE_TYPE_MARQUEE
config = getConfig()
mq = sysv_ipc.MessageQueue(config.getint('message_queue', 'key'), sysv_ipc.IPC_CREAT)
msg = 'Ping!'

parser = OptionParser()

parser.add_option("-t", "--text-scroll", dest="text_scroll",
                                    help="when sent alone, places a simple text message on the marquee queue", metavar="MESSAGE")

(options, args) = parser.parse_args()

msg = options.text_scroll

if msg:
    mq.send(msg, False, MESSAGE_TYPE_MARQUEE)
