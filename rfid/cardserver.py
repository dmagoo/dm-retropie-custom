import logging, time, json
import sysv_ipc

MESSAGE_TYPE_REGISTER = 1
REGISTER_WAIT_TIME = 10

class CardServer:

    def __init__(self, scanner, message_queue, emulationstation, db):
        self.emulationstation = emulationstation
        self.mq = message_queue
        self.scanner = scanner
        self.db = db

    def run(self):
        logging.info("Scanning for RFID Tags")

        register_wait = 0
        t_end = 0
        register_request = None

        for uid in self.scanner.poll_for_scan():

            if register_wait <= 0:
                register_request = self._checkForRegisterRequest()
                if None is not register_request:
                    logging.debug("register request found")
                    if self._validateRegisterRequest(register_request):
                        logging.debug("register request validated")
                        register_wait = REGISTER_WAIT_TIME
                    else:
                        logging.debug("register request not valid")
                    logging.debug("wait time: %i" % (register_wait))


                if register_wait > 0:
                    t_end = time.time() + register_wait
                    logging.info("starting wait period")
                    #debugging... just launch the game when the register message is sent
                    #logging.info("Launching Game")
                    #rom = register_request
                    #logging.info(rom)
                    #try:
                    #self.emulationstation.launchROM(rom["rom"], rom["system"], rom["emulator"])
                    #except Exception, e:
                    #logging.error("Failed to launch ROM: " + str(e) )
                    
            if t_end > 0 and time.time() >= t_end:
                logging.info("ending wait period")
                t_end = register_wait = 0

            if None is not uid:
                logging.info("Card Scanned, UID: %s" % (uid))
                if register_wait > 0 and time.time() < t_end:
                    logging.info("Card Registered")
                    self.db.setRomBinding(
                        uid,
                        register_request["rom"],
                        register_request["system"],
                        register_request["emulator"]
                    )
                    register_wait = 0
                    register_request = None
                else:
                    rom = self.db.getRomBinding(uid)
                    if(rom):
                        logging.info("Launching Game")
                        logging.info(rom)
                        self.emulationstation.launchRom(rom["rom"], rom["system"], rom["emulator"])
                    else:
                        logging.info("Unregistered Card, doing nothing")

    def _checkForRegisterRequest(self):
        """ Return the number of seconds to wait for a register scan"""
        """ TODO: Clear the queue """
        #check queue for latest mode change request
        try:
            m = self.mq.receive(False, MESSAGE_TYPE_REGISTER)
            if m:
                logging.info("register message received")
                logging.info(m)
                return json.loads(m[0])
        except sysv_ipc.BusyError:
            pass

        return None

    def _validateRegisterRequest(self, req):
        return isinstance(req, dict) and "rom" in req and "system" in req
