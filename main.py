import sys
import os
import numpy as np
from glob import glob

from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import (QDir, QTimer)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QShortcut)
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from UI.Ui_MainWindow import Ui_MainWindow
from widgets.BP_Graph import BP_Canvas

from tools.filter import mean_filter

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setup_video()
        self.setup_connection()
        self.show()
        self.canvas_on = False
    def setup_video(self):
        self.BPCanvas = BP_Canvas()
        self.videoGridLayout.addWidget(self.BPCanvas)
        pass
    def setup_connection(self):
        self.actionOpen.triggered.connect(self.open_clicked)
        self.VideoSlider.sliderMoved.connect(self.slider_moved)
        self.singleLeftButton.clicked.connect(self.left_clicked)
        self.doubleLeftButton.clicked.connect(self.left_left_clicked)
        self.singleRightButton.clicked.connect(self.right_clicked)
        self.doubleRightButton.clicked.connect(self.right_right_clicked)
        self.updateButton.clicked.connect(self.BPCanvas.reformat_data)
        self.FrameZeroButton.clicked.connect(self.frame_zero_clicked)
        self.undoButton.clicked.connect(self.undo)
        self.deleteFrameButton.clicked.connect(self.delete_frames_clicked)
        # self.MeanFilterButton.clicked.connect(self.mean_filter_clicked)

        # connect keys
        self.shortcut_j = QShortcut(QKeySequence("Alt+J"), self.centralwidget, self.left_clicked)
        self.shortcut_k = QShortcut(QKeySequence("Alt+K"), self.centralwidget, self.right_clicked)
        self.shortcut_space = QShortcut(QKeySequence("Alt+Space"), self.centralwidget, self.right_clicked)
        pass
    def open_clicked(self):
        video_dir = ''
        DLC_dir = ''
        directory = QFileDialog.getExistingDirectory(None, "Select Directory", QDir.homePath())
        if directory != '' and directory != None:
            filename_key = directory.split('/')[-1]

            # find video filename
            vid_file = glob(directory+"/"+filename_key+'*.avi')
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
                self.VideoSlider.setRange(0, self.BPCanvas.num_frame-1)
                self.VideoSlider.setValue(0)
                self.VideoSlider.setEnabled(True)
                self.frameLabel.setText("0/"+str(self.BPCanvas.num_frame-1))
                self.percentageLabel.setText(str(self.BPCanvas.perc)+"%")
                self.filenameLabel.setText(filename_key)
                self.repaint()
            else:
                print("::FAILED TO LOAD DATA")
                self.reset()
        else:
            self.reset()
        pass
    def slider_moved(self, frame):
        if self.BPCanvas.video_dir != None and self.BPCanvas.DLC_dir != None:
            self.frameLabel.setText(str(frame)+"/"+str(self.BPCanvas.num_frame-1))
            self.BPCanvas.update_canvas(frame)
            self.percentageLabel.setText(str(self.BPCanvas.perc)+"%")
        pass
    def right_clicked(self):
        new_frame = self.BPCanvas.cur_frame+1
        if new_frame < self.BPCanvas.num_frame:
            self.BPCanvas.update_canvas(new_frame)
            self.VideoSlider.setValue(new_frame)
            self.percentageLabel.setText(str(self.BPCanvas.perc)+"%")
            self.frameLabel.setText(str(new_frame)+"/"+str(self.BPCanvas.num_frame-1))
            self.VideoSlider.repaint()
        else:
            print(":: reached the end")
        pass
    def right_right_clicked(self):
        new_frame = self.BPCanvas.cur_frame+2
        if new_frame < self.BPCanvas.num_frame:
            self.BPCanvas.update_canvas(self.BPCanvas.cur_frame+2)
            self.VideoSlider.setValue(new_frame)
            self.percentageLabel.setText(str(self.BPCanvas.perc)+"%")
            self.frameLabel.setText(str(new_frame)+"/"+str(self.BPCanvas.num_frame-1))
            self.VideoSlider.repaint()
        elif new_frame-1 <= self.BPCanvas.num_frame:
            self.BPCanvas.update_canvas(new_frame-1)
            self.VideoSlider.setValue(new_frame-1)
            self.percentageLabel.setText(str(self.BPCanvas.perc)+"%")
            self.frameLabel.setText(str(new_frame)+"/"+str(self.BPCanvas.num_frame-1))
            self.VideoSlider.repaint()
        else:
            print(":: reached the end")
        pass
    def left_clicked(self):
        new_frame = self.BPCanvas.cur_frame-1
        if new_frame >= 0:
            self.BPCanvas.update_canvas(new_frame)
            self.VideoSlider.setValue(new_frame)
            self.percentageLabel.setText(str(self.BPCanvas.perc)+"%")
            self.frameLabel.setText(str(new_frame)+"/"+str(self.BPCanvas.num_frame-1))
            self.VideoSlider.repaint()
        else:
            print(":: reached the beginning")
        pass
    def left_left_clicked(self):
        new_frame = self.BPCanvas.cur_frame-2
        if new_frame >= 0:
            self.BPCanvas.update_canvas(new_frame)
            self.VideoSlider.setValue(new_frame)
            self.percentageLabel.setText(str(self.BPCanvas.perc)+"%")
            self.frameLabel.setText(str(new_frame)+"/"+str(self.BPCanvas.num_frame-1))
            self.VideoSlider.repaint()
        elif new_frame+1 >= 0:
            self.BPCanvas.update_canvas(new_frame+1)
            self.VideoSlider.setValue(new_frame+1)
            self.percentageLabel.setText(str(self.BPCanvas.perc)+"%")
            self.frameLabel.setText(str(new_frame)+"/"+str(self.BPCanvas.num_frame-1))
            self.VideoSlider.repaint()
        else:
            print(":: reached the beginning")
        pass
    def frame_zero_clicked(self):
        if (self.BPCanvas.video_dir != None and self.BPCanvas.DLC_dir != None and 
            self.startLineEdit.text().isdigit()  and self.startLineEdit.text().isdigit()):
            startFr = int(self.startLineEdit.text())
            stopFr = int(self.stopLineEdit.text())+1
            self.startLineEdit.setText("")
            self.stopLineEdit.setText("")
            frame_data = np.ones((self.BPCanvas.num_bp, self.BPCanvas.num_dim-1, stopFr-startFr))*200
            self.BPCanvas.update_frame(frame_data=frame_data, frame=np.arange(startFr,stopFr))
            self.repaint()
        else:
            print(":: no file loaded to filter OR frame not integers")
        pass
    def reset(self):
        self.VideoSlider.setEnabled(False)
        self.percentageLabel.setText("0%")
        self.frameLabel.setText("0/0")
        self.filenameLabel.setText("filename")
        self.BPCanvas.reset()
        self.repaint()
        pass
    def undo(self):
        self.BPCanvas.undo()
        self.repaint()
        pass
    def delete_frames_clicked(self):
        if (self.BPCanvas.video_dir != None and self.BPCanvas.DLC_dir != None):
            ranges=np.array([])
            fr_ranges = self.DeleteLineEdit.text().split(',')
            for interval in fr_ranges:
                frames = interval.split("-")
                if int(frames[0]) <= int(frames[1]):
                    ranges = np.append( ranges, np.arange(int(frames[0]), int(frames[1])+1) )
                else:
                    print(":: incorrect ranges")
            self.BPCanvas.delete_frames(ranges)
        pass
    
    # def mean_filter_clicked(self):
    #     if self.BPCanvas.video_dir != None and self.BPCanvas.DLC_dir != None:
    #         frame_data = mean_filter(data=self.BPCanvas.data, frame=self.BPCanvas.cur_frame, k=1)
    #         self.BPCanvas.update_frame(frame_data=frame_data, frame=self.BPCanvas.cur_frame)
    #         self.repaint()
    #         print(":: finished filtering")
    #     else:
    #         print(":: no file loaded to filter")
    #     pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
















