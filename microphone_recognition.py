#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import webbrowser
from os import path
from interface import ModelInterface
from utils import read_wav
import wave
import numpy as np
import scipy.signal as signal
import pygame
import sys
import os
import random
import time
# obtain audio from the microphone

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something to me")
    audio = r.listen(source)
    print("In processing, please be patient :-)")
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "microphone-results.wav")

src = r.recognize_google(audio)
try:
    rand = random.randint(1, 9)
    print("You said: "+src)
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
        os.system("espeak 'Hi, old friend!' &")
        time.sleep(2)
    elif name_str != newName:
        print("Hi, " + newName + "!")
        os.system("espeak 'Hi' &")
        time.sleep(2)


    if 'hello' in src or 'hi' in src:
        print("Hi! "+newName)
        os.system("espeak 'Hi' &")
    elif 'weather' in src and 'what' in src:
        if 'today' not in src and 'tomorrow' not in src:
            print("Please specific the date.")
            os.system("espeak 'Please specific the date.' &")
            time.sleep(2)
        elif 'today' in src:
            google = 'weather'
            print("Searching on the Internet...")
            os.system("espeak 'Searching on the Internet' &")
            time.sleep(2)
            webbrowser.open('http://www.google.com/search?btnG=1&q=%s'%google)
        else:
            google = 'weather tomorrow'
            print("Searching on the Internet...")
            os.system("espeak 'Searching on the Internet' &")
            webbrowser.open('http://www.google.com/search?btnG=1&q=%s' % google)
    elif 'my' in src and 'neu' in src or 'Neu' in src:
        print("Searching on the Internet...")
        webbrowser.open('https://myneu.neu.edu/cp/home/displaylogin')
    elif 'your' in src and 'favourite' in src and 'color' in src or 'colour' in src:
        print("My favourite color is bule, what about you?")
        os.system("espeak 'My favourite color is bule, what about you?' &")
    elif 'favourite' in src or 'song' in src:
        pygame.init()
        pygame.mixer.init()
        END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(END)
        track = pygame.mixer.music.load("audio/english.wav")
        pygame.mixer.music.play()
        pygame.mixer.music.fadeout(20000)

        while 1:
            for event in pygame.event.get():
                if event.type == END:
                    sys.exit()
    elif 'big' in src and 'data' in src:
        print("Love you! Dino!")
        os.system("espeak 'Love you! Dino!' &")
        time.sleep(2)
    elif 'record' in src and 'voice' in src:
        f = open("tempfile.txt", "rb+")
        f.truncate(0)
        f.write(bytes(src, 'utf8'))
        f.close()
        print("Please open the 'tempfile.txt' to see your voice.")
    elif 'how' in src and 'are' in src and 'you' in src and 'old' not in src:
        print("I am fine, thank you, and you? :-)")
        os.system("espeak 'I am fine, thank you, and you' &")
        time.sleep(2)
    else:
        f = open("tempfile.txt", "rb+")
        f.truncate(0)
        f.write(bytes(src, 'utf8'))
        f.close()
        if rand ==1:
            print("Sorry, I can't understand you.")
            os.system("espeak 'Sorry, I can't understand you.' &")
            time.sleep(2)
        elif rand == 2:
                print("Oh go on.")
                os.system("espeak 'Oh go on.' &")
                time.sleep(2)
        elif rand == 3:
                print("Once again :-)")
                os.system("espeak 'Once again' &")
                time.sleep(2)
        elif rand == 4:
                print("I never really thought about it.")
                os.system("espeak 'I never really thought about it.' &")
                time.sleep(2)
        elif rand == 5:
                print("Maybe you can ask others.")
                os.system("espeak 'Maybe you can ask others.' &")
                time.sleep(2)
        elif rand == 6:
                print("Simple question.")
                os.system("espeak 'Simple question.' &")
                time.sleep(2)
        elif rand == 7:
                print("I am out of working.")
                os.system("espeak 'I am out of working.' &")
                time.sleep(2)
        elif rand == 8:
                print("I'd rather not.")
                os.system("espeak 'I'd rather not.' &")
                time.sleep(2)
        else:
            print("Make it clear.")
            os.system("espeak 'Make it clear.' &")
            time.sleep(2)



except sr.UnknownValueError:
    print("Sorry I don't understand.")
    os.system("espeak 'Sorry I don't understand.' &")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

