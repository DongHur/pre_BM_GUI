import numpy as np

def mean_filter(data, frame, k=5):
    num_frame = data.shape[-1]
    # initialize filtered signal vector
    filtsig = np.copy(data)
    # visual-picked threshold
    threshold = 40
    # find data values above the threshold
    idx_list = np.where( data[:,:,frame]>threshold )[0]
    # implement the running mean filter; each point is the average of k surrounding points
    fr_start = frame-k
    fr_stop = frame+k
    if fr_start<0:
        fr_start = 0
    if fr_stop>num_frame-1:
        fr_stop = num_frame-1
    frame_data = np.mean(data[:,:,fr_start:fr_stop], axis=2)
    return frame_data