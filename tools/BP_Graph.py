import numpy as np
import pandas as pd
import cv2

from PyQt5.QtWidgets import (QWidget)
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.image as mpimg

class BP_Canvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = Figure()
        super(BP_Canvas, self).__init__(self.fig)
        self.video_dir = None
        self.DLC_dir = None
        self.data = None
        self.ax = None
        self.num_frame = 0
        self.num_bp = 30
        self.cur_frame = 0
        self.clicked = False
        self.closest_idx = None
        self.setup_canvas()
    def setup_canvas(self):
        self.ax = self.fig.add_subplot(111)
        self.ax.plot([], 'o-')
        self.ax.set_title('Body Point', fontsize=8)
        self.ax.tick_params(axis='both', labelsize=6)
        self.draw()
        # connect on click graph
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onMotion)
        self.fig.canvas.mpl_connect('button_release_event', self.onUnclick)
        pass
    def load_file(self, video_dir, DLC_dir):
        self.video_dir = video_dir
        self.DLC_dir = DLC_dir
        # setup ant video
        self.cap = cv2.VideoCapture(video_dir)
        # setup DeepLabCut
        bp_h5data = pd.read_hdf(DLC_dir)
        bp_data = bp_h5data[ bp_h5data.keys().levels[0][0] ].values # converts h5 to npy
        self.num_frame = bp_data.shape[0]
        bp_data = np.delete( bp_data.reshape( self.num_frame,self.num_bp,-1 ), obj=-1, axis=2 ) # reformats data and takes out last prob varaiable
        self.data = np.swapaxes(bp_data.T,0,1) # num_bp x num_coord x t
        # udpate video and bodypoint graph
        self.update_canvas(frame=0)
        # cap.release()
        pass
    def update_canvas(self, frame=0):
        self.ax.clear()
        self.cur_frame = frame
        print(":: Current Frame: ", self.cur_frame)
        # update ant video
        self.cap.set(1, frame)
        _, framePic = self.cap.read()
        self.ax.imshow(framePic)
        # update DeepLabCut
        self.plot_bpgraph(frame)
        self.draw()
        pass
    def plot_bpgraph(self, frame=0):
        # self.fig.clear()
        marker = 'o'
        s=4
        # plot graph
        self.ax.plot(self.data[0:4,0,frame], self.data[0:4,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[4:8,0,frame], self.data[4:8,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[8:11,0,frame], self.data[8:11,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[11:14,0,frame], self.data[11:14,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[14:17,0,frame], self.data[14:17,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[17:21,0,frame], self.data[17:21,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[21:24,0,frame], self.data[21:24,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[24:27,0,frame], self.data[24:27,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[27:30,0,frame], self.data[27:30,1,frame], marker=marker, markersize=s)
        pass
    def onClick(self, event):
        if self.DLC_dir and self.video_dir:
            self.clicked = True
            clicked_point = np.array([event.xdata, event.ydata])
            self.closest_idx = self.closest_point(clicked_point)  
        pass
    def onUnclick(self, event):
        self.clicked = False
        self.closest_idx = None
        pass
    def onMotion(self, event):
        if self.clicked == True and self.closest_idx != None:
            print(":: x motion: ", event.xdata)
            print(":: y motion: ", event.ydata)
            clicked_point = np.array([event.xdata, event.ydata])
            self.data[self.closest_idx,:,self.cur_frame] = clicked_point
            self.update_canvas(self.cur_frame)
        pass
    def closest_point(self, clicked_point):
        threshold = 45
        dist_2 = np.sum((self.data[:,:,self.cur_frame] - clicked_point)**2, axis=1)
        closest_idx = np.argmin(dist_2)
        return closest_idx if dist_2[closest_idx] < threshold else None


class BP_Graph(Figure):
    def __init__(self, *args, **kwargs):
        super(BP_Graph, self).__init__()
        self.bp_filepath = ''
        self.num_frame = 0
        self.duration = 1
        self.data = None
    def init_plot(self):
        self.clear()
        ax = self.add_subplot(111)
        ax.plot([], 'o-')
        ax.set_title('Ant Body Point Graph', fontsize=8);
        ax.tick_params(axis='both', labelsize=6);
        pass
    def set_newfile(self, filepath):
        self.bp_filepath = filepath
        self.data = np.load(filepath) # (30,2,5901)
        self.num_frame = self.data.shape[2]
        print("BP_GRAPH Data: ", self.data.shape)
        pass
    def set_duration(self, duration):
        self.duration = duration
        pass
    def update_graph(self, position, frame_data=False):
        if frame_data:
            frame = position # frame as data point
        else:
            frame = int(self.num_frame*position/self.duration)-1 # index is one less; millisecond as data
        self.clear()
        ax = self.add_subplot(111)
        # plot ant points for specific time point t; specific to out setup with 30bp ants
        # data format: num_bp x (X_coord, Y_coord) x t
        # ax.scatter(self.data[:,0,frame], self.data[:,1,frame])
        # graph parameters
        marker = 'o'
        s=4
        # plot graph
        ax.plot(self.data[0:4,0,frame], self.data[0:4,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[4:8,0,frame], self.data[4:8,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[8:11,0,frame], self.data[8:11,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[11:14,0,frame], self.data[11:14,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[14:17,0,frame], self.data[14:17,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[17:21,0,frame], self.data[17:21,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[21:24,0,frame], self.data[21:24,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[24:27,0,frame], self.data[24:27,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[27:30,0,frame], self.data[27:30,1,frame], marker=marker, markersize=s)
        ax.set_xlim(left=-200, right=200)
        ax.set_ylim(bottom=-200, top=200)
        ax.set_aspect('equal', 'box')
        ax.set_title('Ant Body Point Graph', fontsize=8);
        ax.tick_params(axis='both', labelsize=6);
        pass







