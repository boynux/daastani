import json


def playHandler(playback):
    def play(sender, uid, data):
        try:
            obj = json.loads(data)

            if 'key' in obj and obj['key']:
                playback.play(obj['key'])
            else:
                print("RFID tag is not valid!")

        except ValueError:
            print("RFID tag is not valid!")

    return play


def stopHandler(playback):
    def stop(sender, uid):
        playback.stop()

    return stop
