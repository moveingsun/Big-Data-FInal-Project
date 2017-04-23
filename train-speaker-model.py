import os
import itertools
import glob
import argparse
from utils import read_wav
from interface import ModelInterface
from os import path


def task_enroll():
    m = ModelInterface()
    input_dirs = path.dirname(path.realpath(__file__))+ "/Person"
    dirs = os.listdir(input_dirs)
    dirs = [dir for dir in dirs if not os.path.isfile(dir)]
    print(dirs)

    files = []
    if len(dirs) == 0:
        print ("No valid directory found!")
        # sys.exit(1)

    for d in dirs:
        label = os.path.basename(d)
        print(label)
        wavs = glob.glob("Person/"+d+"/*.wav")


        if len(wavs) == 0:
            print ("No wav file found in %s"%(d))
            continue
        for wav in wavs:
            try:
                fs, signal = read_wav(wav)
                m.enroll(label, fs, signal)
                print("wav %s has been enrolled"%(wav))
            except Exception as e:
                print(wav + " error %s"%(e))

        m.train()

if __name__ == "__main__":
    task_enroll()

