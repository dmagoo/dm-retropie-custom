import logging, time
import sysv_ipc

MESSAGE_TYPE_REGISTER = 1
REGISTER_WAIT_TIME = 10

class CardServer:

    def __init__(self, scanner, message_queue, emulationstation, db):
        self.emulationstation = emulationstation
        self.mq = message_queue
        self.scanner = scanner
        self.db = db
        logging.debug("debug")
        logging.info("end init")

    def run(self):
        logging.info("Scanning for RFID Tags")

        register_wait = 0
        t_end = 0
        register_request = None

        for uid in self.scanner.poll_for_scan():

            if register_wait <= 0:
                register_request = self._checkForRegisterRequest()
                if None is not register_request:
                    if self._validateRegisterRequest(register_request):
                        register_wait = REGISTER_WAIT_TIME

                if register_wait > 0:
                    t_end = time.time() + register_wait
                    logging.info("starting wait period")

            if t_end > 0 and time.time() >= t_end:
                logging.info("ending wait period")
                t_end = register_wait = 0

            if None is not uid:
                logging.info("UID")
                if register_wait > 0 and time.time() < t_end:
                    logging.info("Card Registered")
                    self.db.setRomBinding(uid, register_request['rom'], register_request['emulator'])
                    register_wait = 0
                    register_request = None
                else:
                    rom = self.db.getRomBinding(uid)
                    if(rom):
                        logging.info("Launching Game")
                        logging.info(rom)
                        self.emulationstation.launchRom(rom["rom"], rom["emulator"])
                    else:
                        logging.info("Unregistered Card, doing nothing")

    def _checkForRegisterRequest(self):
        """ Return the number of seconds to wait for a register scan"""
        """ TODO: Clear the queue """
        #check queue for latest mode change request
        try:
            m = self.mq.receive(False, MESSAGE_TYPE_REGISTER)
            if m:
                logging.info(m)
                return m
        except sysv_ipc.BusyError:
            pass

        return None

    def _validateRegisterRequest(self, req):
        return isinstance(req, dict) and "rom" in req and "emulator" in req
