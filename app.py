from __future__ import print_function

import os

import RPi.GPIO as GPIO
import MFRC522
import pygame

import handlers

from lib import RFID, Stream, CredentialsProvider, CollisionException, Playback


AWS_IOT_CREDS_URL = os.environ['AWS_IOT_CREDS_URL']
CERT_PEM_PATH = os.environ['CERT_PEM_PATH']
CERT_KEY_PATH = os.environ['CERT_KEY_PATH']


try:
    # initialiations
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)

    driver = MFRC522.MFRC522();
    driver.MFRC522_Init();

    rfid = RFID(driver)

    awsHelper = CredentialsProvider(AWS_IOT_CREDS_URL, (CERT_PEM_PATH, CERT_KEY_PATH))
    playback = Playback(awsHelper, pygame.mixer.music)

    # Event handers
    rfid.onNewCardDetected += lambda sender, uid, data: print("New card has detected: %s (%s)" % (uid, data))
    rfid.onNewCardDetected += handlers.playHandler(playback)

    rfid.onCardRemoved += lambda sender, uid: print("Card %s has removed!" % uid)
    rfid.onCardRemoved += handlers.stopHandler(playback)

    # rfid.onCardStillPresent += lambda sender, uid: print("Card %s is still there!" % uid)

    print("Waiting for tag ...")
    rfid.start()

except CollisionException as e:
    print(e)

except Exception:
    raise

finally:
    GPIO.cleanup()
    pygame.mixer.music.stop()


