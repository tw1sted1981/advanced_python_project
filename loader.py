# Class to deal with loading images and setting up the initial data structure for the machine learning.


import collections
from pprint import pprint

import cv2
import fileseq
from fileseq import filesequence
from mtcnn import MTCNN
import numpy as np


class FrameHandler():
    # add an option to resize in the loader for processing
    def __init__(self, path_to_image_folder):
        self.file_sequence = fileseq.findSequencesOnDisk(path_to_image_folder)[0]
        self.frame_range = self.file_sequence.frameRange().split('-')

        self.file_sequence_data = collections.defaultdict(dict)

        # load in each frame.
        for frame in range(int(self.frame_range[0]), int(self.frame_range[1])+1):
            print('Frame :{}'.format(frame))
            filepath  = self.file_sequence.frame(frame)
            self.file_sequence_data[frame]['image'] = cv2.imread(filepath)   
            self.file_sequence_data[frame]['filepath'] = filepath  








