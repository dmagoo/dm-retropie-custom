import logging, time
import MFRC522

class CardScanner:
    reader = None

    def __init__(self, read_delay, scan_delay):
        self.reader = MFRC522.MFRC522()
        self.read_delay = int(read_delay)
        self.scan_delay = int(scan_delay)

    def poll_for_scan(self):
        continue_reading = True
        while continue_reading:
            time.sleep(self.read_delay)
            # Scan for cards    
            (status,TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
            #print "nope"
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
                    time.sleep(self.scan_delay)
                
            else:
                    yield None
