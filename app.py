from __future__ import print_function

import time
import json
import os

import requests
import boto3
import RPi.GPIO as GPIO
import MFRC522
import pygame

from lib import RFID, Stream

AWS_IOT_CREDS_URL = os.environ['AWS_IOT_CREDS_URL']
CERT_PEM_PATH = os.environ['CERT_PEM_PATH']
CERT_KEY_PATH = os.environ['CERT_KEY_PATH']

pygame.init()
pygame.mixer.init()

res = requests.get(AWS_IOT_CREDS_URL, cert=(CERT_PEM_PATH, CERT_KEY_PATH))

creds = res.json()
# Or via the Session
session = boto3.Session(
    aws_access_key_id=creds['credentials']['accessKeyId'],
    aws_secret_access_key=creds['credentials']['secretAccessKey'],
    aws_session_token=creds['credentials']['sessionToken']
)

# s3resource = session.resource('s3')
# bucket = s3resource.Bucket('daastani')
s3 = session.client('s3', region_name='eu-central-1')


def play(sender, uid, data):
    obj = json.loads(data)

    if 'key' in obj:
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


try:
    pygame.mixer.music.set_volume(1.0)

    driver = MFRC522.MFRC522();
    driver.MFRC522_Init();

    rfid = RFID(driver)

    def newCardDetected(sender, uid, data):
        print("New card has detected: %s (%s)" % (uid, data))


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


