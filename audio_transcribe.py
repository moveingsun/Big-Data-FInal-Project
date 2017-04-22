#!/usr/bin/env python3

import speech_recognition as sr
from os import path
import webbrowser
from interface import ModelInterface
from utils import read_wav
import pygame
import sys

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "audio/zhu1.wav")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

src = r.recognize_google(audio)

# recognize speech using Google Speech Recognition
try:
    m = ModelInterface.load(path.join(path.dirname(path.realpath(__file__)), "model.out"))
    fs, signal = read_wav(AUDIO_FILE)
    newName = m.predict(fs, signal)
    f = open("temp.txt","rb+")
    name = f.readline()
    f.truncate(0)
    f.write(bytes(newName, 'utf8'))
    f.close()
    name_str = name.decode('utf8')
    if newName in name_str:
        print("Hi, old friend!")
    elif name_str != newName:
        print("Hi, " + newName + "!")

    if 'hello' in src or 'hi' in src:
        print("Hi!")
    elif 'weather' and 'what' in src:
        if 'today' not in src and 'tomorrow' not in src:
            print("Please specific the date.")
        elif 'today' in src:
            google = 'weather'
            print("Searching on the Internet...")
        # webbrowser.open('http://www.google.com/search?btnG=1&q=%s'%google)
        else:
            google = 'weather tomorrow'
            print("Searching on the Internet...")
            webbrowser.open('http://www.google.com/search?btnG=1&q=%s' % google)
    elif 'myneu' in src:
        print("Searching on the Internet...")
        webbrowser.open('https://myneu.neu.edu/cp/home/displaylogin')
    elif 'your' in src and 'favourite' in src and 'color' in src or 'colour' in src:
        print("My favourite color is bule, what about you?")
    elif 'favourite' in src and 'song' in src:
        pygame.init()
        pygame.mixer.init()
    # screen = pygame.display.set_mode([640,480])
    # pygame.mixer.music.set_volume(0.5)
        END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(END)
        track = pygame.mixer.music.load("english.wav")
        pygame.mixer.music.play()
        pygame.mixer.music.fadeout(20000)

        while 1:
            for event in pygame.event.get():
                if event.type == END:
                    sys.exit()
    elif 'big' in src and 'data' in src:
        print("Love you! Dino!")
    elif 'record' in src and 'voice' in src:
        f = open("temp.txt", "rb+")
        f.truncate(0)
        f.write(bytes(src, 'utf8'))
        f.close()
    elif 'How' in src and 'are' in src and 'you' in src and 'old' not in src:
        print("I am fine, thank you, and you? :-)")
    else:
        f = open("temp.txt", "rb+")
        f.truncate(0)
        f.write(bytes(src, 'utf8'))
        f.close()


except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


