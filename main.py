import sys
import os
import numpy as np

# from PyQt5.QtGui import 
# from PyQt5.QtCore import 
from PyQt5.QtWidgets import QApplication, QMainWindow

from UI.Ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.show()





if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainWin = MainWindow()
	ret = app.exec_()
	sys.exit(ret)