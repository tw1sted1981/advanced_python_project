#******************************************************************************
# content       = Face detection
#               Should be able to point this at a folder with an image sequence
#               and it will find the face and return the text to create an 
#               animated crop node within nuke. 
#                 
#
# version       = 0.0.1
# date          = 2022-01-08
#
# dependencies  = 
# todos         = NEXT - build point class, with functions to convert coordinate 
#               origin axis.
#
# author        = Chris Forrester <chrisforrester.tv@gmail.com>
#******************************************************************************



import time
import logging
import argparse
from pprint import pprint
from collections import defaultdict

import cv2
import numpy as np
from mtcnn import MTCNN

from point import Point
import loader
import nuke_node_builder as nnb


def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="Path to the directory with")
    args = vars(ap.parse_args())

    # load image sequence to use
    face = loader.FrameHandler(args["folder"])
    face.user_select_sequence()

    # create the detector, using default weights
    detector = MTCNN()

    start_time = time.time()

    first_frame     = face.first_frame()
    last_frame      = face.last_frame()+1

    # dict used for animation later on.  
    nuke_animation = defaultdict(lambda: defaultdict(dict))
    for frame in range(first_frame, last_frame,):
        print('Processing frame {:>3} of {:<3}'.format(frame, last_frame, ))
        face.load_frame(frame, 100, 100)

        # detect faces in the image
        face.add_mtcnn_data(frame, detector.detect_faces(face.image(frame)))

        img_width, img_height = face.image_dimensions(frame)

        for face_detection in face.get_mtcnn_data(frame):
            # compute the (x, y)-coordinates of the bounding box for the
            startX, startY, width, height = face_detection['box']
            p1 = Point(startX, startY, img_width, img_height)
            p2 = Point(startX + width, startY + height, img_width, img_height) 

            top_left_x, top_left_y         = p1.point()
            bottom_right_x, bottom_right_y = p2.point()

            nuke_animation[frame]['x1'] = top_left_x
            nuke_animation[frame]['y1'] = top_left_y
            nuke_animation[frame]['x2'] = bottom_right_x
            nuke_animation[frame]['y2'] = bottom_right_y

            # draw box around face        
            a = cv2.rectangle(face.image(frame), (startX, startY), (startX + width, startY + height),
                (0, 0, 255), 1) 
            cv2.imshow("Image with face drawn", a)
            cv2.waitKey(2)
            
            face.remove_image(frame)

    # create animated curve
    pprint(nuke_animation)
    x1 = y1 = x2 = y2 = ''

    #sorted_dict = dict(sorted(nuke_animation.items()))
    for frame in range(first_frame, last_frame,):
        logging.info(frame)
        x1 += nnb.create_frame_value(frame, nuke_animation[frame]['x1'])
        y1 += nnb.create_frame_value(frame, nuke_animation[frame]['y1'])
        x2 += nnb.create_frame_value(frame, nuke_animation[frame]['x2'])
        y2 += nnb.create_frame_value(frame, nuke_animation[frame]['y2'])

    x1_anim = nnb.create_animation_curve(x1)
    y1_anim = nnb.create_animation_curve(y1)
    x2_anim = nnb.create_animation_curve(x2)
    y2_anim = nnb.create_animation_curve(y2)

    animation_curve_list = [x1_anim, y1_anim, x2_anim, y2_anim]
    animated_crop =nnb.create_crop(animation_curve_list)
    print(animated_crop)
    print('Total time to process was {} '.format(time.time() - start_time))

if __name__ == '__main__':
    main()