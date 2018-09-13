[![Build Status](https://travis-ci.org/boynux/daastani.svg?branch=master)](https://travis-ci.org/boynux/daastani)

# Daastani

## What's this?

Daastani is a simple application which turns a RaspberryPi into a Jukebox, I created this for my son to enjoy listening to bed time stories.

## Prototype

[![Watch this video](https://i.ytimg.com/vi/u3LzA0zzYi4/0.jpg)](https://www.youtube.com/watch?v=u3LzA0zzYi4")

## How to run?

You need:

* RasspberryPi
* Active Speaker or Amp + Speaker
* SPI enabled
* Docker installed
* AWS IoT service configured
* AWS IoT certs are copied to RPi to `/etc/daastani/certs`
* The Following ENV vars in `/etc/default/daastani`
  * `AWS_IOT_CREDS_URL="https://<iot device id>.credentials.iot.<aws region>.amazonaws.com/role-aliases/<IAM Role name to access S3 bucket>/credentials"`
  * `CERT_KEY_PATH="/etc/daastani/certs/daastani-private.pem.key"`
  * `CERT_PEM_PATH="/etc/daastani/certs/daastani-certificate.pem.crt"`


    docker run --rm --name daastani -it --privileged --env-file /etc/default/daastani -v /etc/daastani/certs:/etc/daastani/certs --device=/dev/snd --group-add=audio --group-add=adm --group-add=997 --group-add=999  boynux/daastani:armhf-1


## How it works?

Using RFID reader connected to RPi, and utilizing AWS IoT framework Daastani is able to play different audio streams when a registered RFID tag is near the detector. The audio keeps playing as long as the tags is still present, upon removal of the tag the audio playback stops.

I put the whole device in a box with RFID read near the surface, then I attached some RFID tags inside some stuffed animals and dolls and toys, once the toy is placed on top of the box the story (audio) starts to play and by changing the tag a different story can be played back.

## Terminology

in Persian *Daastani* means: Related to a story. Or Something that's worth to be told as a story!
