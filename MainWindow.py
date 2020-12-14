from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import pyqtgraph as pg
import matplotlib.pyplot as plt
import wave
import numpy as np
import os
import librosa
import simpleaudio as sa

class MainWindow(QtWidgets.QWidget):

    # Constructor
    def __init__(self):
        super().__init__()

        # Title
        self.appHeader = QtWidgets.QLabel('<h2 style="text-align: center">Gender Voice Detection</h2>', alignment = QtCore.Qt.AlignAbsolute)

        # Waveform widget
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Path title
        self.pathTitle = QtWidgets.QLabel('<p>File Path: </p>', alignment = QtCore.Qt.AlignCenter)

        # Path value
        self.pathValue = QtWidgets.QLabel('<p style=\'font-weight: bold\'>N/A</p>', alignment = QtCore.Qt.AlignCenter)

        # Gender title
        self.genderTitle = QtWidgets.QLabel('<p>Detected gender: </p>', alignment = QtCore.Qt.AlignCenter)

        # Gender value
        self.genderValue = QtWidgets.QLabel('<p style=\'font-weight: bold\'> Not detected yet</p>', alignment = QtCore.Qt.AlignCenter)

        # Upload button
        self.uploadButton = QtWidgets.QPushButton('Upload')

        #Layouts

        self.mainLayout = QtWidgets.QGridLayout()
        self.pathLayout = QtWidgets.QHBoxLayout()
        self.genderLayout = QtWidgets.QHBoxLayout()

        # Set row stretching for each row in GridLayout
        self.mainLayout.setRowStretch(0, 1)
        self.mainLayout.setRowStretch(1, 5)
        self.mainLayout.setRowStretch(2, 1)
        self.mainLayout.setRowStretch(3, 1)
        self.mainLayout.setRowStretch(4, 1)

        self.pathLayout.addWidget(self.pathTitle)
        self.pathLayout.addWidget(self.pathValue)

        self.genderLayout.addWidget(self.genderTitle)
        self.genderLayout.addWidget(self.genderValue)

        # Bind widgets to main window
        self.mainLayout.addWidget(self.appHeader)
        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addLayout(self.pathLayout, 2, 0)
        self.mainLayout.addLayout(self.genderLayout, 3, 0)
        self.mainLayout.addWidget(self.uploadButton)

        self.setLayout(self.mainLayout)

        self.audioFilePath = ""

        # Apply CSS Rules
        self.applyLayoutRules()

        # Trigger FileDialog on click
        self.uploadButton.clicked.connect(lambda: self.setOnUploadListener())


    # Method that applies CSS rules to self attributes
    def applyLayoutRules(self):

        # Upload button
        self.uploadButton.setStyleSheet("""
            QPushButton {
                width: 35%;
                height: 25%;
                margin: 0 auto;
            }
        """)


    # Upload click listener
    def setOnUploadListener(self):

        fileDialog = QtWidgets.QFileDialog.Options()
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select audio file...", "", 
                                                    "WAV Audio Files (*.wav)", options = fileDialog)

        if files and len(files) == 1:
            self.audioFilePath = files[0]
            self.pathValue.setText(files[0])
        else:
            Exception("Cannot pass multiple files.")

        audioObj = wave.open(self.audioFilePath, mode = 'r')
        self.generateWaveform(audioObj)
        self.getGender()


    # Generate waveform method
    def generateWaveform(self, audioObj):
        frames = audioObj.readframes(-1)
        frames = np.fromstring(frames, dtype = np.int16)

        sampleFreq = audioObj.getframerate()

        time = np.linspace(0, len(frames) / sampleFreq, num = len(frames))

        # Draw plt figure
        self.figure.clear()
        axis = self.figure.add_subplot(111)
        axis.plot(time, frames)

        # Draw to canvas
        self.canvas.draw()


    def getGender(self):

        X, sample_rate = librosa.load(self.audioFilePath, res_type = 'kaiser_fast', sr = 22050, offset = 0.5)
        sample_rate = np.array(sample_rate)

        f0, voiced_flag, voiced_probs = librosa.pyin(X, fmin = 50, fmax = 1900)

        # Inlocuiesc campurile NAN din array-ul F0 cu 0 (zero) ca sa pot calcula valorile pitch-ului
        f0_no_nan_values = np.where(np.isnan(f0), 0, f0)

        # Calculez max pitch ca fiind valoarea maxima ce se gaseste in structura de date np.array F0_NO_NAN_VALUES
        f0_max = np.max(f0_no_nan_values)

        print(f0_max)
        print(f0_no_nan_values)

        averageFreq = 0
        count = 0

        for i in f0_no_nan_values:
            if(i != 0):
                averageFreq += i
                count += 1

        averageFreq /= count

        print(averageFreq)


        if averageFreq >= 0 and averageFreq <= 210:
            self.genderType = 'Male'
        elif averageFreq > 210 and averageFreq <= 600:
            self.genderType = 'Female'
        elif averageFreq > 600:
            self.genderType = 'Child'

        self.genderValue.setText(self.genderType)
        self.playSound()

    def playSound(self):

        wave_obj = sa.WaveObject.from_wave_file(self.audioFilePath)
        play_obj = wave_obj.play()
        play_obj.wait_done()

        







    
