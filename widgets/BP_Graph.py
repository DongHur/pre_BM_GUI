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
        self.num_dim = 3
        self.perc = 0
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
        store = pd.HDFStore(DLC_dir, mode='r')
        bp_data = store.select('df_with_missing').T.to_numpy()
        store.close()
        # bp_h5data = pd.read_hdf(DLC_dir)
        # bp_data = bp_h5data[ bp_h5data.keys().levels[0][0] ].values # converts h5 to npy

        self.num_frame = bp_data.shape[-1]
        self.data  = bp_data.reshape(self.num_bp,self.num_dim,self.num_frame) # num_bp x num_coord x t
        # udpate video and bodypoint graph
        self.update_canvas(frame=0)
        # cap.release()
        pass
    def update_canvas(self, frame=0):
        self.ax.clear()
        self.cur_frame = frame
        self.perc = round(np.mean(self.data[:,2,frame])*100, 2)
        # print(":: Current Frame: ", self.cur_frame)
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
            # print(":: x motion: ", event.xdata)
            # print(":: y motion: ", event.ydata)
            clicked_point = np.array([event.xdata, event.ydata])
            self.data[self.closest_idx,0:2,self.cur_frame] = clicked_point
            self.update_canvas(self.cur_frame)
        pass
    def closest_point(self, clicked_point):
        threshold = 45
        dist_2 = np.sum((self.data[:,0:2,self.cur_frame] - clicked_point)**2, axis=1)
        closest_idx = np.argmin(dist_2)
        return closest_idx if dist_2[closest_idx] < threshold else None
    def update_frame(self, frame_data, frame):
        self.data[:,:,frame] = frame_data
        self.update_canvas(frame)
        pass
    def reformat_data(self):
        if self.DLC_dir:
            store = pd.HDFStore(self.DLC_dir, mode='a')
            df = store['df_with_missing']
            df.iloc[:,:] = self.data.reshape(self.num_bp*self.num_dim, self.num_frame).T
            store.put(key='df_with_missing', value=df)
            store.close()
            print(":: finished updating database")
        else:
            print(":: no files uploaded")
        pass
    def reset(self):
        self.video_dir = None
        self.DLC_dir = None
        self.data = None
        self.num_frame = 0
        self.cur_frame = 0
        self.perc = 0
        self.clicked = False
        self.closest_idx = None
        self.ax.clear()
        self.setup_canvas()
        pass






