import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

class soundHub(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.filePaths = []
        self.currentIndex = -1

        self.layout = QVBoxLayout()

        self.loadButton = QPushButton('Select Files', self)
        self.loadButton.clicked.connect(self.selectFiles)
        self.layout.addWidget(self.loadButton)

        self.spectrogramLabel = QLabel(self)
        self.layout.addWidget(self.spectrogramLabel)

        self.playButton = QPushButton('Play Audio', self)
        self.playButton.clicked.connect(self.playAudio)
        self.layout.addWidget(self.playButton)

        self.stopButton = QPushButton('Stop Audio', self)
        self.stopButton.clicked.connect(self.stopAudio)
        self.layout.addWidget(self.stopButton)

        self.yesButton = QPushButton('Yes', self)
        self.noButton = QPushButton('No', self)
        self.maybeButton = QPushButton('Maybe', self)
        self.layout.addWidget(self.yesButton)
        self.layout.addWidget(self.noButton)
        self.layout.addWidget(self.maybeButton)

        self.nextButton = QPushButton('Next', self)
        self.nextButton.clicked.connect(self.nextFile)
        self.nextButton.setEnabled(False)
        self.layout.addWidget(self.nextButton)

        self.prevButton = QPushButton('Previous', self)
        self.prevButton.clicked.connect(self.prevFile)
        self.prevButton.setEnabled(False)
        self.layout.addWidget(self.prevButton)

        self.label = QLabel('No file loaded', self)
        self.numberLabel = QLabel('', self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.numberLabel)

        self.setWindowTitle('SoundHub Annotater')

        self.setLayout(self.layout)

    def selectFiles(self):
        # underscore ignores the filter return (wav filter)
        fileNames, _ = QFileDialog.getOpenFileNames(self, 'Select Files', '', 'Audio Files (*.wav)')
        self.filePaths = fileNames
        self.currentIndex = 0
        self.loadAudio(fileNames[0])
        self.updateButtonStates()

    def loadAudio(self, filePath):
        self.label.setText(f"{filePath}")
        self.generateSpectrogram(filePath)

        self.audio_data, self.sr = librosa.load(filePath, sr = None)

    def playAudio(self):
        try:
            sd.play(self.audio_data, self.sr)

        except Exception as e:
            self.showError(str(e))

    def stopAudio(self):
        sd.stop()
    
    def nextFile(self):
        if self.currentIndex < len(self.filePaths) - 1:
            self.currentIndex += 1
            self.stopAudio()
            self.loadAudio(self.filePaths[self.currentIndex])
            self.updateButtonStates()

    def prevFile(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.stopAudio()
            self.loadAudio(self.filePaths[self.currentIndex])
            self.updateButtonStates()
    
    def updateButtonStates(self):
        self.prevButton.setEnabled(self.currentIndex > 0)
        self.nextButton.setEnabled(self.currentIndex < len(self.filePaths) - 1)
        self.label.setText(f'{self.filePaths[self.currentIndex]}')
        self.numberLabel.setText(f'{self.currentIndex + 1}/{len(self.filePaths)}')

    def generateSpectrogram(self, file_name):
        y, sr = librosa.load(file_name)
        s = librosa.feature.melspectrogram(y = y, sr = sr)
        s_db = librosa.power_to_db(s, ref = np.max)
        librosa.display.specshow(s_db, cmap = 'gray_r', sr=sr, x_axis='time', y_axis='mel')

        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel-frequency spectrogram')

        plt.savefig('spectrogram.png')
        plt.close()

        pixmap = QPixmap('spectrogram.png')
        self.spectrogramLabel.setPixmap(pixmap)
    
    def showError(self, errorMessage):
        errorDialog = QMessageBox()
        errorDialog.setIcon(QMessageBox.Critical)
        errorDialog.setWindowTitle("Error")
        errorDialog.setInformativeText(errorMessage)
        errorDialog.setStandardButtons(QMessageBox.Ok)
        errorDialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = soundHub()
    ex.show()
    sys.exit(app.exec_())