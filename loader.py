# Class to deal with loading images and setting up the initial data structure for the machine learning.
# create a load file function
# create a cache all function
# merge sequence and frame range under the same dict as everything else

import logging
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

    def user_select_sequence(self):
        # allow the user to select the sequence the object will work with
        pass

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

    def load_frame(self, frame, scale_x = 100, scale_y = 100):
        filepath = self.file_sequence_data[self.sequence_name]['file_sequence'].frame(frame)
        image = resized_image = cv2.imread(filepath)
        img_height, img_width, _, = image.shape

        if (scale_x != 100) and (scale_y != 100):
            # resize image based on arguments passed
            img_width = int(image.shape[1] * scale_x / 100)
            img_height = int(image.shape[0] * scale_y / 100)
            dim = (img_width, img_height)
            resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)  

        logging.info('loading frame {:08} - scale_x ={}, scale_y ={}'.format(frame, scale_x, scale_y))
        self.file_sequence_data[self.sequence_name][frame]['filepath'] = filepath  
        self.file_sequence_data[self.sequence_name][frame]['image'] = resized_image
        self.file_sequence_data[self.sequence_name][frame]['height'] = img_height     
        self.file_sequence_data[self.sequence_name][frame]['width'] = img_width   

    def load_all_frames(self, scale_x = 100, scale_y = 100):
        for frame in range(self.first_frame(), self.last_frame()+1):
            self.load_frame(frame, scale_x, scale_y)

    def remove_image(self, frame):
        self.file_sequence_data[self.sequence_name][frame]['image'] = None        
        logging.info('removing image on frame {:08}'.format(frame,))

    def image(self, frame):
        return self.file_sequence_data[self.sequence_name][frame]['image'] 

    def image_dimensions(self, frame):
        return [self.file_sequence_data[self.sequence_name][frame]['width'], 
                self.file_sequence_data[self.sequence_name][frame]['height'],
            ]
