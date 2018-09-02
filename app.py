from __future__ import print_function

import time
import json
import os

import requests
import boto3
import RPi.GPIO as GPIO
import MFRC522
import pygame

from lib import RFID, Stream, CredentialsProvider, CollisionException

AWS_IOT_CREDS_URL = os.environ['AWS_IOT_CREDS_URL']
CERT_PEM_PATH = os.environ['CERT_PEM_PATH']
CERT_KEY_PATH = os.environ['CERT_KEY_PATH']

awsHelper = CredentialsProvider(AWS_IOT_CREDS_URL, (CERT_PEM_PATH, CERT_KEY_PATH))
stream = None  # This is a global variable, since we are using one stream at a time consier a singleton object

def play(sender, uid, data):
    global stream

    try:
        obj = json.loads(data)
    
        if 'key' in obj:
            session = awsHelper.getSession()
            s3 = session.client('s3', region_name='eu-central-1')

            signedUrl = s3.generate_presigned_url(
                ClientMethod = "get_object",
                ExpiresIn = 3600,
                HttpMethod = 'GET',
                Params = {
                    "Bucket": "daastani",
                    "Key": obj['key'],
                    }
                )

            stream = Stream(signedUrl)

            pygame.mixer.music.load(stream)
            pygame.mixer.music.play()
        else:
            print("RFID tag is not valid!")

    except ValueError:
        print("RFID tag is not valid!")


try:
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)

    driver = MFRC522.MFRC522();
    driver.MFRC522_Init();

    rfid = RFID(driver)

    rfid.onNewCardDetected += lambda sender, uid, data: print("New card has detected: %s (%s)" % (uid, data))
    rfid.onNewCardDetected += play

    rfid.onCardRemoved += lambda sender, uid: print("Card %s has removed!" % uid)
    rfid.onCardRemoved += lambda sender, uid: stream.close()

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


