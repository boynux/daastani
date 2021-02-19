#!/usr/bin/python

from __future__ import print_function

import os
import signal
import sys

import RPi.GPIO as GPIO
import MFRC522
# import pygame

import handlers

import time
import asyncio
from functools import wraps, partial

from lib import RFID, CredentialsProvider, CollisionException, Playback


AWS_IOT_CREDS_URL = os.environ['AWS_IOT_CREDS_URL']
CERT_PEM_PATH = os.environ['CERT_PEM_PATH']
CERT_KEY_PATH = os.environ['CERT_KEY_PATH']


def sigterm_handler(signo, stack_frame):
    print("Stopping...")
    sys.exit(0)


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run 


async def main():
    # initialiations
    # pygame.init()
    # pygame.mixer.init()
    # pygame.mixer.music.set_volume(1.0)

    driver = MFRC522.MFRC522()
    driver.MFRC522_Init()

    rfid = RFID(driver)

    awsHelper = CredentialsProvider(AWS_IOT_CREDS_URL, (CERT_PEM_PATH, CERT_KEY_PATH))
    playback = Playback(awsHelper, None) # pygame.mixer.music)

    # Event handers
    # rfid.onNewCardDetected += lambda sender, uid, data: print("New card has detected: %s (%s)" % (uid, data))
    rfid.onNewCardDetected += handlers.playHandler(playback)

    # rfid.onCardRemoved += lambda sender, uid: print("Card %s has removed!" % uid)
    rfid.onCardRemoved += handlers.stopHandler(playback)

    # rfid.onCardStillPresent += lambda sender, uid: print("Card %s is still there!" % uid)

    print("Waiting for tag ...")
    await rfid.start()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        start = time.time()
        asyncio.run(main())
        end = time.time()

        print(f"Time elapse: {end-start}")
    except CollisionException as e:
        print(e)

    except Exception:
        raise

    finally:
        GPIO.cleanup()
        # pygame.mixer.music.stop()
