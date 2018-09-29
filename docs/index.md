---
title: ""
---

# Intro

I have a 6 years old son, like any other kid at this age, ke likes listening to bed time stories.
Me and his mom, always make time for him to tell one or two stories every night. However in reality it's not always that easy!

The other day I was till very late and my wife was also tired. When I got home, my son asked me to read him some stories.
Of course I did that as usual, no matter how tired I was, but he asked for the third and fourth stories.
It's not easy to tell your little kid that you are tired, this happens quite a few times every month that he simply wants to 
hear more and more stories. If you are a parent, you probably know that.

Sometimes we try to play some recorded stores for him using normal speakers.
However he usually rejects that, I don't know why, but he does not like them at all.

One weekend, at his birthday, I decided to give him a spcial gift. Something which is innovative and unique, and maybe he likes.
That's how *Daasatani* born!

# What is Daastani?

Daastani is a *Story Box*, and with that my little kid can listen to bedtime stories that he likes, at his will.
I record stories myself. The beauty of Daastani is that, it's simple to use at night. 

It consists of a simple card board box, wrapped in gift wrapping paper (I need to improve that). There are some RFID cards 
(They are like a small keychain or business cards) each has a different ID, which is assiciated to 
a different story. My son just picks his favorite card, puts it on top of the boxand done, story starts to play!

# How difficult is to build one?

You don't need to have a deep understanding of electronics and IoT, although a little bit knowledge about that doesn't hurt.
You need to know basisc of RaspberryPi, Docker and you are going to need a little bit of patience too.

There are some wiring involved which I used breadboards for that matter to avoid soldering.
Since nothing is exposed to the outside of the box, except the charging port, breadboards work just fine.
I also used hot glue gun to fix parts in their place firmly.

# Prerequisites

* 1 x [RaspberryPi unit (model 3 or zero)](https://www.adafruit.com/product/3708) ~ €14
* 1 x [SD Card 8+ GB](https://www.google.de/search?tbm=shop&q=sd+card+9gb) ~ €4
* 1 x [2-4 W 8 ohm speaker](https://www.amazon.de/gp/product/B00Y0IZD5K/) ~ €4
* 1 x [Adafruit I2S MAX98357A Amplifier](https://www.adafruit.com/product/3006) ~ €6
* 1 x [RC522 RFID + couple of RFID tags](https://www.google.de/search?tbm=shop&q=rc522+rfid&oq=rc522+rfid) ~ €2
* 1 x Micro USB charger
* Breadboard and jumper wires
* Mobile phone rechargable battery pack (optional)

All items except battery and powr supply should cost you about €30 or cheaper.


# How to build it?

*Be aware that the majority of these steps are manual. I didn't have time to automate it. If you're obsesses with automation feel free to make a PR with your awesome scripts*

The fun part begins ....

## Cooke a pie

1. Probably the easiest part, unpack your RaspberryPi and SD Card. Follow the [official instruction](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
2. Mount the SD card in your computer, and create an empty file called `ssh` in `/boot` partition. eg. `touch /Volumes/boot/ssh` on Mac
3. Now put SD card in your RPi and plug the **Lan Cabel** and power, boot it up!
4. After a short while you should be able to `ssh` to your Pi, `ssh pi@192.168.0.x` (Check your router for the correct IP). hint: password is: `raspberry`
5. Configure your Wifi connection using `raspi-config`.
6. Install Docker `curl https://get.docker.com | bash` :screem:
7. Once done, shutdown your Pi and follow the next steps.

## Make some wiring mess

There are two components to connect to your Pi:

### Adafruit I2S MAX98357A Amplifier

Follow the [official instructions](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/assembly) to connect the amplifier. Make sure you complete the installations of drivers as well.

When you finished the installation you should be able to play some test sounds using your Raspberry Pi, like:

`speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav`

### MFRC522 RFID reader

There are several tutorials online on how to install the RFID reader to RPi. I recommend this post: [How to setup a Raspberry Pi RFID RC522 Chip](https://pimylifeup.com/raspberry-pi-rfid-rc522/)

If you ran into any issues with the setup, leave me a comment, but it should be easy and straight forward.

## Install Daastani

To be continued ...
