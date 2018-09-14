import json


def playHandler(playback):
    def play(sender, uid, data):
        try:
            obj = json.loads(data.strip())

            if 'key' in obj and obj['key']:
                playback.play(obj['key'])
            else:
                print("RFID tag is not valid!", obj)

        except ValueError as e:
            print("RFID tag is not valid!", e)

    return play


def stopHandler(playback):
    def stop(sender, uid):
        playback.stop()

    return stop
