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

from mtcnn import MTCNN
import numpy as np
import cv2

from point import Point
import loader
import nuke_node_builder as nnb



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True, help="Path to the directory with")
args = vars(ap.parse_args())

# load image sequence to use
face = loader.FrameHandler(args["folder"])
face.print_sequences()
select_sequence = int(input('type sequence to use : '))
face.select_sequence(select_sequence)

# dict used for animation later on.  
nuke_animation = defaultdict(lambda: defaultdict(dict))

# create the detector, using default weights
detector = MTCNN()

start_time = time.time()

first_frame     = face.first_frame()
last_frame      = face.last_frame()+1

for frame in range(first_frame, last_frame,):
    print('Processing frame {:>3} of {:<3}'.format(frame, last_frame, ))
    face.load_frame(frame, 100, 100)

    # detect faces in the image
    faces = detector.detect_faces(face.image(frame))
    pprint(faces)

    img_width = face.image_dimensions(frame)[0]
    img_height = face.image_dimensions(frame)[1]

    for face_detection in faces:
        # compute the (x, y)-coordinates of the bounding box for the
        startX, startY, width, height = face_detection['box']

        top_left      = Point(startX, startY, img_width, img_height)
        bottom_right  = Point(startX + width, startY + height, img_width, img_height)

        nuke_animation[frame]['x1'] = top_left.point_in_nuke()[0]
        nuke_animation[frame]['y1'] = top_left.point_in_nuke()[1]
        nuke_animation[frame]['x2'] = bottom_right.point_in_nuke()[0]
        nuke_animation[frame]['y2'] = bottom_right.point_in_nuke()[1]

        crop =nnb.create_crop(top_left.point_in_nuke() + bottom_right.point_in_nuke())
        #logging.info(crop)
        
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
