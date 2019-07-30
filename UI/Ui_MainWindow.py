# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(689, 775)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.videoDisplayWidget = QtWidgets.QWidget(self.centralwidget)
        self.videoDisplayWidget.setGeometry(QtCore.QRect(20, 30, 651, 511))
        self.videoDisplayWidget.setAutoFillBackground(False)
        self.videoDisplayWidget.setObjectName("videoDisplayWidget")
        self.updateButton = QtWidgets.QPushButton(self.centralwidget)
        self.updateButton.setGeometry(QtCore.QRect(290, 690, 113, 32))
        self.updateButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.updateButton.setObjectName("updateButton")
        self.divider = QtWidgets.QFrame(self.centralwidget)
        self.divider.setGeometry(QtCore.QRect(20, 620, 651, 20))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.divider.setFont(font)
        self.divider.setFrameShape(QtWidgets.QFrame.HLine)
        self.divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.divider.setObjectName("divider")
        self.filter1Button = QtWidgets.QPushButton(self.centralwidget)
        self.filter1Button.setGeometry(QtCore.QRect(20, 640, 113, 32))
        self.filter1Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.filter1Button.setObjectName("filter1Button")
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setGeometry(QtCore.QRect(110, 570, 71, 31))
        self.playButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.playButton.setObjectName("playButton")
        self.filenameLabel = QtWidgets.QLabel(self.centralwidget)
        self.filenameLabel.setGeometry(QtCore.QRect(310, 10, 60, 16))
        self.filenameLabel.setObjectName("filenameLabel")
        self.VideoSlider = QtWidgets.QSlider(self.centralwidget)
        self.VideoSlider.setGeometry(QtCore.QRect(10, 550, 661, 22))
        self.VideoSlider.setOrientation(QtCore.Qt.Horizontal)
        self.VideoSlider.setObjectName("VideoSlider")
        self.frameInputBox = QtWidgets.QLineEdit(self.centralwidget)
        self.frameInputBox.setGeometry(QtCore.QRect(300, 570, 121, 21))
        self.frameInputBox.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.frameInputBox.setAlignment(QtCore.Qt.AlignCenter)
        self.frameInputBox.setObjectName("frameInputBox")
        self.singleLeftButton = QtWidgets.QPushButton(self.centralwidget)
        self.singleLeftButton.setGeometry(QtCore.QRect(60, 570, 51, 31))
        self.singleLeftButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.singleLeftButton.setObjectName("singleLeftButton")
        self.doubleLeftButton = QtWidgets.QPushButton(self.centralwidget)
        self.doubleLeftButton.setGeometry(QtCore.QRect(10, 570, 51, 31))
        self.doubleLeftButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.doubleLeftButton.setObjectName("doubleLeftButton")
        self.singleRightButton = QtWidgets.QPushButton(self.centralwidget)
        self.singleRightButton.setGeometry(QtCore.QRect(180, 570, 51, 31))
        self.singleRightButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.singleRightButton.setObjectName("singleRightButton")
        self.doubleRightButton = QtWidgets.QPushButton(self.centralwidget)
        self.doubleRightButton.setGeometry(QtCore.QRect(230, 570, 51, 31))
        self.doubleRightButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.doubleRightButton.setObjectName("doubleRightButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 689, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.updateButton.setText(_translate("MainWindow", "Update"))
        self.filter1Button.setText(_translate("MainWindow", "Filter"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.filenameLabel.setText(_translate("MainWindow", "Filename"))
        self.frameInputBox.setPlaceholderText(_translate("MainWindow", "0"))
        self.singleLeftButton.setText(_translate("MainWindow", "<"))
        self.doubleLeftButton.setText(_translate("MainWindow", "<<"))
        self.singleRightButton.setText(_translate("MainWindow", ">"))
        self.doubleRightButton.setText(_translate("MainWindow", ">>"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open ..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
