import speech_recognition as sr
import webbrowser
from os import path
from interface import ModelInterface
from utils import read_wav
import pygame
import sys
import os
import random
import time
import wave
import numpy as np
import pyaudio
from scipy.io import wavfile
from python_speech_features import mfcc


def recognition():
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 22050
        RECORD_SECONDS = 5
        filename = "microphone-results.wav"
        WAVE_OUTPUT_FILENAME = filename
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=chunk)

        print("Say something to me")
        all = []
        for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
            data = stream.read(chunk)
            all.append(data)
        print("In processing, please be patient :-)")

        stream.close()
        p.terminate()

        # write data to WAVE file


        data = b''.join(all)
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()

        r = sr.Recognizer()
        # with sr.Microphone() as source:

        #    audio = r.listen(source)

        #    with open("microphone-results.wav", "wb") as f:
        #        f.write(audio.get_wav_data())
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "microphone-results.wav")
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)
        # src = r.recognize_google(audio)
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""
        {
          "type": "service_account",
          "project_id": "friendly-lamp-165519",
          "private_key_id": "3d845d2c7a13ad656a1a07a84c69d073e0dbebcb",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDjq+rIrWZWTxkT\njTE3//csOpZdiCc+N+gik4echrg04TsHjorGUsuIgVUPzB+mJgT4wB2ZtqT5T3iu\nQ33h3uSul8IPlkSVkoVtpIfyzQPcUB9Q71JsDZTKPTg2TQZLlmQhOj4ch80gC0kD\n+Qg5Vi+BGgsYrlTYRsgbub7OuzuCsxEgtIfxRHiLHeLNMNtHUnax5y5O910JcRKk\naB4zncN86jfkYn0nCiq11M5PuatcoDLAyvram4PkFfVvhJMKG1G/bM61REc1wL3+\nRvEIOGePkykA8ACSSl5kHPqHoCMH1+e1lIX9qNtxtxo2Sq2fRuPOAe/7VLn3kVe7\nfWOHawvdAgMBAAECggEBAJ7gi9k62F2GmTNBpoUzxKNCx0fCCdCrZv0qAsrCYK3W\nN0FQwZsgkBRUXK3HfpaNlY6ZUo7AHGQ2hzrksmX7C46jLLN/46CVPTOES7KuSvFl\noFT0jYoF+D0hd6a9HZWF/54IbOuwAP9JoMx67rhEYqYvLGsuzNqYmnBusK7HjgHn\n7x5RtD6oOj86vWWK+nrfWPoBcn2QpgDNhKh8fBk/jZPw50PXiTPwMoWyc06I0NXa\ni4hRfTLQ50eV8cyxDdI83PweusomyS1CIDzEvs+VU+resV86v+FxaBZok27e7RMv\n/WonoeTsyfdVDJIYQ9zJ81GpFZR7y22kbklI2TTef2kCgYEA9ZvhMtJcpttHC3jH\nWkIx6cT9nC4L7acD2v9JNHa4Dqf+PPTzP1RkjeZVQK5tZzlpr75pEox1rl3HnhAg\nbDqmvUUYlps/Py6wVYLyx+khFsfsh3eP6vIWyD4ZhQ5pL3bGw9bd7YKBFmL+beSu\n+s5LdsopPPGLOwBinlVxq8j/dPMCgYEA7U3DV7dKpR8250UjyqEN8ejVwKlIHHQm\nuXEaAZuD5pX9tOTlOLiFT9gljLTgqWTmAr3LjDwFsTRq7Q9I9KYV3KuFrKCTqV9G\nVo2jeDan+J3mk5OhIibwfDuSWt2cZwK5v0qvUYi+EjbFoz6Jw5pq/DE336/e+ALK\n7kwiQDnK7+8CgYBuWG5A6wn9XR76JHVMM9lA8eQPOxDY4OR2i6NUEtJ2ozsyH8r5\ndO0IY6eBu9wjOEQnVSDX2Is2n6ODfDNU7LTk7Boz7+Pmew92G7L/5dmb5o55/lmG\ncOWTaXMFuIfBb1e1vN9QSgW9DRTKQqfqvqxg3krQuqSXCYFFKZY8W72JyQKBgEP3\n2PJ/wjaHOT+GcxjvhkH6kXasRcY4knrc5Tj+pQnffhpY0Tqsxyo2W5Lwn8SE7Mhu\nOiXBb1PxEosxrJC+HVbmHdRy7bg+XLQfv2mIJhY0i71LNITGqGy810+FV+29PxyG\nNK7ivqYS4ArAt865pNj08+7yvadFjYAxeEHzC6grAoGAImz2Nr20BagdtZO6xQ0O\nXW2SK31Ho/G969bCk5NPRH0gcTjVFR+RcmG7IcfFfbx1FCiw0X96E//Ou2xdB0Cs\naGOGjmsjhJ/6LRXtOaMw1P+a8MV7emQkpJuwc/Aib4XCg0BEIGPCSCZq6tds/ULz\nBBg4jz14SUto6ltGLa8lnJg=\n-----END PRIVATE KEY-----\n",
          "client_email": "speechproject@friendly-lamp-165519.iam.gserviceaccount.com",
          "client_id": "108776166391900514665",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://accounts.google.com/o/oauth2/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/speechproject%40friendly-lamp-165519.iam.gserviceaccount.com"
        }
        """
        srcUP = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        src = srcUP.lower()

        try:
            rand = random.randint(1, 9)
            print("You said: " + src)
            m = ModelInterface.load(path.join(path.dirname(path.realpath(__file__)), "model.out"))
            fs, signal = read_wav(AUDIO_FILE)
            newName = m.predict(fs, signal)
            f = open("temp.txt", "rb+")
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
                if newName == "Menglu":
                    os.system("espeak 'Hi, Menglu' &")
                elif newName == "Zhan":
                    os.system("espeak 'Hi, Zhan' &")
                elif newName == "Yuxing":
                    os.system("espeak 'Hi, Yuxing' &")
                elif newName == "Yankai":
                    os.system("espeak 'Hi, Yankai' &")
                else:
                    os.system("espeak 'Hi there' &")
                time.sleep(2)

            if 'hello' in src or 'hi' in src or 'Hi' in src or 'Hello' in src:
                print("Hi! " + newName)
                os.system("espeak 'Hi' &")
            elif 'good' in src and 'bye' not in src and 'Bye' not in src:
                if 'morning' in src:
                    print("Good morning")
                    os.system("espeak 'Good morning' &")
                elif 'evening' in src:
                    print("Good evening")
                    os.system("espeak 'Good evening' &")
                else:
                    print("Yeah, that's good.")
                    os.system("espeak 'Yeah, that's good.' &")
                time.sleep(2)
            elif ('who' in src and 'you' in src) or ('what' in src and 'your' in src and 'name' in src):
                print("I am spark.")
                os.system("espeak 'I am spark ' &")
                time.sleep(2)
            elif 'weather' in src and ('what' in src or 'how' in src or 'How' in src or 'What' in src):
                if 'today' not in src and 'tomorrow' not in src:
                    print("Please specific the date.")
                    os.system("espeak 'Please specific the date.' &")
                    time.sleep(2)
                elif 'today' in src:
                    google = 'weather'
                    print("Searching on the Internet...")
                    os.system("espeak 'Searching on the Internet' &")
                    time.sleep(2)
                    webbrowser.open('http://www.google.com/search?btnG=1&q=%s' % google)
                else:
                    google = 'weather tomorrow'
                    print("Searching on the Internet...")
                    os.system("espeak 'Searching on the Internet' &")
                    webbrowser.open('http://www.google.com/search?btnG=1&q=%s' % google)
            elif ('my' in src or 'My' in src) and ('neu' in src or 'Neu' in src):
                print("Searching on the Internet...")
                os.system("espeak 'Searching on the Internet' &")
                webbrowser.open('https://myneu.neu.edu/cp/home/displaylogin')
            elif 'joke' in src:
                print("HaHaHaHaHaHa hahahahahahaha.")
                os.system("espeak 'HaHaHaHaHaHa hahahahahahaha.' &")
                time.sleep(2)
            elif 'your' in src and 'favorite' in src and 'color' in src or 'colour' in src:
                print("My favourite color is bule, what about you?")
                os.system("espeak 'My favourite color is bule, what about you?' &")
            elif 'favorite' in src or 'song' in src:
                pygame.init()
                pygame.mixer.init()
                END = pygame.USEREVENT + 1
                pygame.mixer.music.set_endevent(END)
                track = pygame.mixer.music.load("audio/Shape of You.mp3")
                pygame.mixer.music.play()
                pygame.mixer.music.fadeout(15000)

                while 1:
                    for event in pygame.event.get():
                        if event.type == END:
                            sys.exit()
                print("Do you like it? ;-)")
                os.system("espeak 'Do you like it?'&")
                time.sleep(2)
            elif 'big' in src or 'Big' in src and 'data' in src:
                print("Love you! Dino!")
                os.system("espeak 'Love you! Dino!' &")
                time.sleep(2)
            elif 'Goodbye' in src or 'goodbye' in src or 'bye' in src or 'Bye' in src:
                print("Bye! ;-)")
                os.system("espeak 'Bye' &")
                time.sleep(2)
            elif 'record' in src and 'Record' in src:
                char = src.find('record') + 7
                spilt = src[char:]
                f = open("tempfile.txt", "rb+")
                f.truncate(0)
                f.write(bytes(spilt, 'utf8'))
                f.close()
                print("Finished")
                os.system("espeak 'Finished' &")
                print("Please open the 'tempfile.txt' to see your voice.")
            elif 'how' in src and 'are' in src and 'you' in src and 'old' not in src:
                print("I am fine, thank you, and you? :-)")
                os.system("espeak 'I am fine, thank you, and you' &")
                time.sleep(2)
            elif 'who' in src and 'i' in src and 'am' in src:
                print("Lovely question, I think you are " + newName)
                os.system("espeak 'Lovely question' &")
                time.sleep(2)
            else:
                f = open("tempfile.txt", "rb+")
                f.truncate(0)
                f.write(bytes(src, 'utf8'))
                f.close()
                if 'search' in src or 'Search' in src:
                    char = src.find('search') + 7
                    spilt = src[char:]
                    print("Searching on the Internet...")
                    os.system("espeak 'Searching on the Internet' &")
                    webbrowser.open('http://www.google.com/search?btnG=1&q=%s' % spilt)
                    time.sleep(2)
                elif 'what' in src or 'What' in src:
                    char = src.find('what') + 5
                    spilt = src[char:]
                    print("Searching on the Internet...")
                    os.system("espeak 'Searching on the Internet' &")
                    webbrowser.open('http://www.google.com/search?btnG=1&q=%s' % spilt)
                    time.sleep(2)
                elif rand == 1:
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
                    print("I would rather not.")
                    os.system("espeak 'I would rather not.' &")
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

def read_wav(fname):
    fs, signal = wavfile.read(fname)
    assert len(signal.shape) == 1, "Only Support Mono Wav File!"
    return fs, signal

def get_feature(fs, signal):
    mfcc_feature = mfcc(signal, fs)
    if len(mfcc_feature) == 0:
        print >> sys.stderr, "ERROR.. failed to extract mfcc feature:", len(signal)
    return mfcc_feature



if __name__ == '__main__':
    recognition()
