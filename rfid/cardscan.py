import logging, time
import MFRC522

SCAN_DELAY = 10
registered_games = {"62,170,161,185" : ["0", "_SYS_", "nes", "/home/pi/RetroPie/roms/nes/Megaman.nes"]}

class CardScanner:
    reader = None

    def __init__(self):
        self.reader = MFRC522.MFRC522()

    def poll_for_scan(self):
        #print "I"
        #yield '123'
        #time.sleep(100)
        continue_reading = True
        while continue_reading:
            
            # Scan for cards    
            (status,TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)

            # If a card is found
            if status == self.reader.MI_OK:
                logging.info("Card detected")
            
                # Get the UID of the card
                (status,uid) = self.reader.MFRC522_Anticoll()

                # If we have the UID, continue
                if status == self.reader.MI_OK:
                    # Print UID
                    uid = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
                    logging.info("Card read UID: " + uid)
                    yield uid
                    time.sleep(SCAN_DELAY)
                
