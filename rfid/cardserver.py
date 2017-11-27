import logging, time
import sysv_ipc
from emulationstation import EmulationStation

MESSAGE_TYPE_REGISTER = 1

registered_games = {"62,170,161,185" : ["0", "_SYS_", "nes", "/home/pi/RetroPie/roms/nes/Megaman.nes"]}

class CardServer:

    def __init__(self, scanner, message_queue):
        self.mq = message_queue
        self.scanner = scanner
        logging.debug("debug")
        logging.info("end init")

    def run(self):
        logging.info("Scanning for RFID Tags")

        register_wait = 0
        t_end = 0

        for uid in self.scanner.poll_for_scan():
            if register_wait <= 0:
                register_wait = int(self._checkForRegisterRequest())
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
                    register_wait = 0
                else:
                    if(registered_games.get(uid)):
                        game = registered_games.get(uid)
                        logging.info("Launching Game")
                        logging.info(game)
                        #call([self.launch_cmd] + game)
                    else:
                        logging.info("Unregistered Card")

    def _checkForRegisterRequest(self):
        """ Return the number of seconds to wait for a register scan"""
        """ TODO: Clear the queue """
        #check queue for latest mode change request
        try:
            m = self.mq.receive(False, MESSAGE_TYPE_REGISTER)
            if m:
                logging.info(m)
                return 10
        except sysv_ipc.BusyError:
            pass

        return 0

                    
    def registerUIDGameLaunch(self, uid, emulator, rom_path):
        pass

    def getUIDGameLaunch(self, uid, emulator, rom_path):
        pass

    def readRegistrationFile(self):
        pass

    def writeRegistrationFile(self):
        pass    
