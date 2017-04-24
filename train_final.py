import os
import glob
from utils import read_wav
from interface import ModelInterface
from os import path
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore


def train_model():
    m = ModelInterface()
    input_dirs = path.dirname(path.realpath(__file__)) + "/Person"
    dirs = os.listdir(input_dirs)
    dirs = [dir for dir in dirs if not os.path.isfile(dir)]
    print(dirs)
    QApplication.processEvents()

    files = []
    if len(dirs) == 0:
        print ("No valid directory found!")
        QApplication.processEvents()
        # sys.exit(1)

    for d in dirs:
        label = os.path.basename(d)
        print(label)
        QApplication.processEvents()
        wavs = glob.glob("Person/" + d + "/*.wav")

        if len(wavs) == 0:
            print ("No wav file found in %s" % (d))
            QApplication.processEvents()
            continue
        for wav in wavs:
            try:
                fs, signal = read_wav(wav)
                m.enroll(label, fs, signal)
                print("wav %s has been enrolled" % (wav))
                QApplication.processEvents()
            except Exception as e:
                print(wav + " error %s" % (e))
                QApplication.processEvents()

        m.train()
        #m.dump(ModelInterface.load(path.join(path.dirname(path.realpath(__file__)), "model.out")))
        m.dump("model.out")
        print('finished Training!')
        QApplication.processEvents()

if __name__ == '__main__':
    train_model()

