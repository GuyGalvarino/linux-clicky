#!/usr/bin/env python

from os import listdir, getcwd
from random import choice
from third_party.evdev import DeviceGroup
from linux_clicky.play_sound import PlaySound
from linux_clicky.detect_keyboards import detect_keyboards
from argparse import ArgumentParser

parser = ArgumentParser(description='linux-clicky')
parser.add_argument('-v', action="store", default=1, dest='volume')

results = parser.parse_args()

# Get a list of sound files
sounds = listdir(getcwd() + '/sounds')
sound_tmp = {}
sound_tmp["click"] = []
for sound in sounds:
    if sound == 'enter.wav':
        sound_tmp["enter"] = sound
    elif sound == 'space.wav':
        sound_tmp["space"] = sound
    else:
        sound_tmp["click"].append(sound)
sounds = sound_tmp
# Volume: Negative to lower the volume
volume = str(results.volume)

dev = DeviceGroup(detect_keyboards())
while 1:
    event = dev.next_event()
    if event is not None:
        # print repr(event)
        if event.type == "EV_KEY" and event.value == 1:
            if event.code.startswith("KEY"):
                if event.code == "KEY_ENTER":
                    filename = getcwd() + '/sounds/' + sounds["enter"]
                elif event.code == "KEY_SPACE":
                    filename = getcwd() + '/sounds/' + sounds["space"]
                else:
                    filename = getcwd() + '/sounds/' +\
                        choice(sounds["click"])
                PlaySound(filename, volume).start()
