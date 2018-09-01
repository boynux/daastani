from __future__ import print_function

import time

import RPi.GPIO as GPIO
import MFRC522
import pygame

from lib import RFID


pygame.init()
pygame.mixer.init()

#load the sound file
pygame.mixer.music.load("127221_380.mp3")
pygame.mixer.music.set_volume(1.0)




try:
    driver = MFRC522.MFRC522();
    driver.MFRC522_Init();

    rfid = RFID(driver)

    def newCardDetected(sender, uid):
        print("New card has detected: %s" % uid)


    rfid.onNewCardDetected += newCardDetected
    rfid.onNewCardDetected += lambda sender, uid: pygame.mixer.music.rewind()
    rfid.onNewCardDetected += lambda sender, uid:  pygame.mixer.music.play()

    rfid.onCardRemoved += lambda sender, uid: print("Card %s has removed!" % uid)
    rfid.onCardRemoved += lambda sender, uid: pygame.mixer.music.stop()

    # rfid.onCardStillPresent += lambda sender, uid: print("Card %s is still there!" % uid)
    rfid.start()

except Exception as e:
    print(e)
finally:
    GPIO.cleanup()
    pygame.mixer.music.stop()


