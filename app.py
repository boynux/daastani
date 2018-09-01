from __future__ import print_function

import time

import requests
import RPi.GPIO as GPIO
import MFRC522
import pygame

from lib import RFID, Stream


pygame.init()
pygame.mixer.init()


UIDMap = {
    556273207803: "http://niniban.com/files/fa/news/1395/2/21/124544_208.mp3"
}

def play(sender, uid):
    if uid in UIDMap:
        stream = Stream(UIDMap[uid])

        pygame.mixer.music.load(stream)
        pygame.mixer.music.play()
    else:
        print("RFID tag is not valid!")


try:
    pygame.mixer.music.set_volume(1.0)

    driver = MFRC522.MFRC522();
    driver.MFRC522_Init();

    rfid = RFID(driver)

    def newCardDetected(sender, uid):
        print("New card has detected: %s" % uid)


    rfid.onNewCardDetected += newCardDetected
    rfid.onNewCardDetected += play

    rfid.onCardRemoved += lambda sender, uid: print("Card %s has removed!" % uid)
    rfid.onCardRemoved += lambda sender, uid: pygame.mixer.music.stop()

    # rfid.onCardStillPresent += lambda sender, uid: print("Card %s is still there!" % uid)
    rfid.start()

except Exception as e:
    print(e)

finally:
    GPIO.cleanup()
    pygame.mixer.music.stop()


