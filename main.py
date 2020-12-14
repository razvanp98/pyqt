from MainWindow import MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui

import sys

appInstance = QtWidgets.QApplication([])

main = MainWindow()
main.setWindowTitle('Gender Voice Detection')
main.resize(800, 800)
main.show()

sys.exit(appInstance.exec_())
