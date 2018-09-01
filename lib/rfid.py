import time

from lib.event import Event


class RFID:

    Key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
    BlockAddrs = [8, 9, 10]

    def __init__(self, driver):
        self._driver = driver

        self.onNewCardDetected = Event()
        self.onCardRemoved = Event()
        self.onCardStillPresent = Event()

    def start(self):
        while True:
            time.sleep(0.1)  # replace with timer

            uid, data = self._waitForNewCard()
            if not uid:
                continue

            self._newCardDetected(uid, data)
            while True:
                if self._checkIfCardPresent():
                    self._cardStillPresent(uid)
                    time.sleep(0.1)
                else:
                    self._cardIsRemoved(uid)
                    break


    def _waitForNewCard(self):
        status, bits = self._driver.MFRC522_Request(self._driver.PICC_REQIDL);

        if status != self._driver.MI_OK:
            return None, None

        status, uid = self._driver.MFRC522_Anticoll()
        if status != self._driver.MI_OK:
            raise Exception("Could not call anti collision successfully!", status, uid)

        return self._uid_to_num(uid), self._readData(uid)


    def _readData(self, uid):
        self._driver.MFRC522_SelectTag(uid)
        status = self._driver.MFRC522_Auth(self._driver.PICC_AUTHENT1A, 11, self.Key, uid)
        data = []
        if status == self._driver.MI_OK:
            for block_num in self.BlockAddrs:
                block = self._driver.MFRC522_Read(block_num) 
                if block:
                    data += block
        self._driver.MFRC522_StopCrypto1()

        return ''.join(chr(i) for i in data)


    def _checkIfCardPresent(self):
        control = 0x1

        for i in range(2):
            status, bits = self._driver.MFRC522_Request(self._driver.PICC_REQIDL);
            if status != self._driver.MI_OK:
                status, uid = self._driver.MFRC522_Anticoll()
                if status == self._driver.MI_OK:
                    control |= 0xFF

                control = control << 1
            control = control << 1;


        if control == 0x08: 
            return True
        else:
            return False

    def _newCardDetected(self, *args):
        self.onNewCardDetected(self, args)

    def _cardIsRemoved(self, *args):
        self.onCardRemoved(self, args)

    def _cardStillPresent(self, *args):
        self.onCardStillPresent(self, args)

    def _uid_to_num(self, uid):
        n = 0
        for i in range(0, 5):
            n = n * 256 + uid[i]
        return n

