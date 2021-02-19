import time
import asyncio

from lib.event import Event


class CollisionException(Exception):
    pass


class RFID:

    Key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    BlockAddrs = [8, 9, 10]

    def __init__(self, driver):
        self._driver = driver

        self.onNewCardDetected = Event()
        self.onCardRemoved = Event()
        self.onCardStillPresent = Event()

    async def start(self):
        while True:
            # time.sleep(0.1)  # replace with timer

            uid, data = await self._async_waitForNewCard()
            # if not uid:
            #    continue

            await self._newCardDetected(uid, data)
            # while True:
            #     time.sleep(0.3)
            #    if self._checkIfCardPresent():
            await self._async_cardRemoved()
            await self._cardIsRemoved(uid)
            #         self._cardStillPresent(uid)
            #    else:
            #        self._cardIsRemoved(uid)
            #        break

    async def _async_waitForNewCard(self):
        while True:
            status, bits = self._driver.MFRC522_Request(self._driver.PICC_REQIDL)

            if status != self._driver.MI_OK:
                # return None, None
                await asyncio.sleep(0.3)
                continue

            status, uid = self._driver.MFRC522_Anticoll()
            if status != self._driver.MI_OK:
                raise CollisionException("Could not call anti collision successfully!", status, uid)

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

    async def _async_cardRemoved(self):
        while True:
            if self._checkIfCardPresent():
                await asyncio.sleep(0.5)
            else:
                return

    def _checkIfCardPresent(self):
        control = 0x1

        for i in range(2):
            status, bits = self._driver.MFRC522_Request(self._driver.PICC_REQIDL)
            if status != self._driver.MI_OK:
                status, uid = self._driver.MFRC522_Anticoll()
                if status == self._driver.MI_OK:
                    control |= 0xFF

                control = control << 1
            control = control << 1

        if control == 0x08:
            return True
        else:
            return False

    async def _newCardDetected(self, *args):
        await asyncio.gather(*self.onNewCardDetected(self, args))

    async def _cardIsRemoved(self, *args):
        await asyncio.gather(*self.onCardRemoved(self, args))

    def _cardStillPresent(self, *args):
        self.onCardStillPresent(self, args)

    def _uid_to_num(self, uid):
        n = 0
        for i in range(0, 5):
            n = n * 256 + uid[i]
        return n
