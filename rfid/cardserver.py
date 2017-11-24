import logging
MODE_LAUNCH = 0
MODE_REGISTER = 1
mode = MODE_REGISTER

cmd = "/opt/retropie/supplementary/runcommand/runcommand.sh"
registered_games = {"62,170,161,185" : ["0", "_SYS_", "nes", "/home/pi/RetroPie/roms/nes/Megaman.nes"]}

class CardServer:

    def __init__(self, scanner, mode=MODE_REGISTER):
        self.scanner = scanner
        self.mode = mode
        logging.debug("debug")
        logging.info("end init")

    def run(self):
        logging.info("Scanning for RFID Tags")
        print self.scanner
        for uid in self.scanner.poll_for_scan():
            if MODE_LAUNCH == self.mode:
                if(registered_games.get(uid)):
                    game = registered_games.get(uid)
                    logging.info("Launching Game")
                    logging.info(game)
                    #call([cmd] + game)
                else:
                    logging.info("Unregistered Card")
            elif MODE_REGISTER == self.mode:
                    logging.info("Card Registered")
                    #sys.exit(0)

                
