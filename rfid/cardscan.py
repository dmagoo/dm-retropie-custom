import logging, time
import MFRC522

#so the same card does not get continuously read
SCAN_DELAY = 10
#make a 2 second delay between loops to save cpu
READ_DELAY = 2
registered_games = {"62,170,161,185" : ["0", "_SYS_", "nes", "/home/pi/RetroPie/roms/nes/Megaman.nes"]}

class CardScanner:
    reader = None

    def __init__(self):
        self.reader = MFRC522.MFRC522()

    def poll_for_scan(self):
        continue_reading = True
        while continue_reading:
            time.sleep(READ_DELAY)
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
                
