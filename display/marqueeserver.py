import logging, time
import sysv_ipc
from animation import TextScroll

MESSAGE_TYPE_MARQUEE = 2
READ_DELAY = 2

class MarqueeServer:

    def __init__(self, matrix,  message_queue):
        self.mq = message_queue
        self.matrix = matrix
        logging.debug("debug")
        logging.info("end init")

    def run(self):
        logging.info("Waiting for marquee reqest")

        continue_polling = True
        while continue_polling:
            time.sleep(READ_DELAY)
            try:
                req = self._checkForMarqueeRequest()
                if req:
                    logging.info('message received ' + str(req))
                    self.performTextScroll(req)
            except sysv_ipc.BusyError:
                pass

    def performTextScroll(self, marqueeText):
        anim = TextScroll(marqueeText, self.matrix._master_surface.rect)
        print "starting animation"
        for tick in anim.run(self.matrix._master_surface):
            time.sleep(1/20.0)
            self.matrix.write().strip.show()

    def _checkForMarqueeRequest(self):
        """ Return the number of seconds to wait for a register scan"""
        """ TODO: Clear the queue """
        #check queue for latest mode change request
        try:
            m = self.mq.receive(False, MESSAGE_TYPE_MARQUEE)
            if m:
                logging.info(m)
                return m[0]
        except sysv_ipc.BusyError:
            pass

        return None
