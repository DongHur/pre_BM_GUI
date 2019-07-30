import sys
import os
import numpy as np
from glob import glob

# from PyQt5.QtGui import 
from PyQt5.QtCore import (QDir)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog)
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from UI.Ui_MainWindow import Ui_MainWindow
from tools.BP_Graph import BP_Canvas

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setup_video()
        self.setup_connection()
        self.show()
    def setup_connection(self):
        self.actionOpen.triggered.connect(self.open_clicked)
        self.VideoSlider.sliderMoved.connect(self.slider_moved)
        # self.updateButton.clicked.connect()
        # self.filter1Button.clicked.connect()
        # self.playButton.clicked.connect()
        # self.singleLeftButton.clicked.connect()
        # self.doubleLeftButton.clicked.connect()
        # self.singleRightButton.clicked.connect()
        # self.doubleRightButton.clicked.connect()

        # self.VideoSlider.setValue(position)
        pass
    def setup_video(self):
        self.BPCanvas = BP_Canvas()
        self.videoGridLayout.addWidget(self.BPCanvas)
        pass
    def open_clicked(self):
        video_filename = ''
        DLC_filename = ''
        directory = QFileDialog.getExistingDirectory(None, "Select Directory", QDir.homePath())
        if directory != '' or directory != None:
            filename_key = directory.split('/')[-1]

            # find video filename
            vid_file = glob(directory+"/"+filename_key+'.avi')
            if len(vid_file) != 0:
                video_dir = vid_file[0]
            else:
                print("::Could Not Find Video File: "+directory+"/"+filename_key+".avi")

            # find DeepLabCut filename
            DLC_file = glob(directory+"/"+filename_key+"*.h5")
            if len(vid_file) != 0:
                DLC_dir = DLC_file[0]
            else:
                print("::Could Not Find DeepLabCut File: "+directory+"/"+filename_key+"*.h5")

            if video_dir!='' and DLC_dir!='':
                self.BPCanvas.load_file(video_dir, DLC_dir)
                # update slider
                self.VideoSlider.setRange(0, self.BPCanvas.num_frame)
            else:
                print("::FAILED TO LOAD DATA")
        pass
    def slider_moved(self, frame):
        self.BPCanvas.update_canvas(frame)
        pass





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
















