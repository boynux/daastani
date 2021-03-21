import json


def playHandler(playback):
    async def play(sender, uid, data):
        try:
            obj = json.loads(data.strip())

            if 'key' in obj and obj['key']:
                await playback.play(obj['key'])
            else:
                print("RFID tag is not valid!", obj)

        except ValueError as e:
            print("RFID tag is not valid!", e)

    return play


def stopHandler(playback):
    async def stop(sender, uid):
        await playback.stop()

    return stop
