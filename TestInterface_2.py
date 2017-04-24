import sys,time
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
#import helloworld
import train_final 
from train_final import *
#import microphone_final
#from microphone_final import *
import microphone_recognition_final
from microphone_recognition_final import *
import audio_final
from audio_final import *

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Voice Recogenize'
        self.initUI()


        
    def flush(self):
        pass

    def initUI(self):
        self.setWindowTitle(self.title)

        self.setGeometry(300, 300, 700, 500)
 
        button = QPushButton('Train', self)
        button.setToolTip('Training the data')
        button.move(50,50) 
        button.clicked.connect(self.on_click)
 
        button2 = QPushButton('Microphone', self)
        button2.setToolTip('Using the Microphone')
        button2.move(50,100) 
        button2.clicked.connect(self.on_click_2)

        button3 = QPushButton('Audio', self)
        button3.setToolTip('Using the Audio')
        button3.move(50,150) 
        button3.clicked.connect(self.on_click_3) 

        button4 = QPushButton('clear', self)
        button4.setToolTip('Clear the console')
        button4.move(50,200) 
        button4.clicked.connect(self.on_click_4) 

        self.my_text_edit = QTextEdit(self)
        self.my_text_edit.move(200,50)
        self.my_text_edit.setReadOnly(True)
        self.my_text_edit.resize(400,350)

        
        self.process = QProcess(self)
        self.process.readyRead.connect(self.dataReady)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        self.show()

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
      
    @pyqtSlot()
    def on_click(self):

        self.process.start(train_final.train_model())

    def on_click_2(self):
        print('Using the Microphone to test')

        self.process.start(microphone_recognition_final.recognition())

    def on_click_3(self):
        print('Using the Audio to test')
        self.process.start(audio_final.audioRecognition())

    def on_click_4(self):
        print('Using the Audio to test')
        self.my_text_edit.setText('')

    @QtCore.pyqtSlot(str)
    def on_myStream_message(self, message):
        self.initUI().my_text_edit.moveCursor(QtGui.QTextCursor.End)
        self.initUI().my_text_edit.insertPlainText(message)


    def append(self, text):
        cursor = self.initUI().my_text_edit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        self.output.ensureCursorVisible()

    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput())
        self.append(text)

    def __del__(self):

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__  
          
    def normalOutputWritten(self, text):  
        cursor = self.my_text_edit.textCursor()  
        cursor.movePosition(cursor.End)  
        cursor.insertText(text)
        self.my_text_edit.setTextCursor(cursor)
        self.my_text_edit.ensureCursorVisible()

    def dataReady(self):
        cursor = self.my_text_edit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(str(self.process.readAll()))
        self.my_text_edit.ensureCursorVisible()

class EmittingStream(QtCore.QObject):  
    textWritten = QtCore.pyqtSignal(str) 
    def write(self, text):  
        self.textWritten.emit(str(text))

class MyStream(QtCore.QObject):
    message = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


