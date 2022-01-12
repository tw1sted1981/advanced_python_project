# Class to deal with loading images and setting up the initial data structure for the machine learning.
# create a load file function
# create a cache all function
# merge sequence and frame range under the same dict as everything else

from collections import defaultdict
from pprint import pprint

import cv2
import fileseq
from mtcnn import MTCNN
import numpy as np

class FrameHandler():
    # add an option to resize in the loader for processing
    def __init__(self, path_to_image_folder):
        self.path_to_image_folder = path_to_image_folder

        self.file_sequence_data = defaultdict(lambda: defaultdict(dict)) #collections.defaultdict(dict)

    def print_sequences(self):
        for index, sequence in enumerate(fileseq.findSequencesOnDisk(self.path_to_image_folder)):
            print('{:<3} - {}'.format(index, sequence[index]))

    def select_sequence(self, sequence_index):
        self.sequence_name = str(sequence_index)
        # when sequence is selected updated the inital bits of the dict
        self.file_sequence_data[self.sequence_name]['file_sequence'] = fileseq.findSequencesOnDisk(self.path_to_image_folder)[sequence_index]
        self.file_sequence_data[self.sequence_name]['frame_range'] = self.file_sequence_data[self.sequence_name]['file_sequence'].frameRange().split('-')

    def status(self,):
        pprint(self.file_sequence_data)

    def frame_range(self,):
        return list(map(int, self.file_sequence_data[self.sequence_name]['frame_range']))

    def first_frame(self,):
        return int(self.file_sequence_data[self.sequence_name]['frame_range'][0])

    def last_frame(self,):
        return int(self.file_sequence_data[self.sequence_name]['frame_range'][1])

    def load_frame(self, frame):
        filepath = self.file_sequence_data[self.sequence_name]['file_sequence'].frame(frame)

        print('loading frame {:08}'.format(frame))
        self.file_sequence_data[self.sequence_name][frame]['filepath'] = filepath  
        self.file_sequence_data[self.sequence_name][frame]['image'] = cv2.imread(filepath)  

    def load_all_frames(self):
        for frame in range(self.first_frame(), self.last_frame()):
            self.load_frame(frame)

    def image(self, frame):
        return self.file_sequence_data[self.sequence_name][frame]['image'] 
        