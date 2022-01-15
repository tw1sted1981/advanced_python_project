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

face = loader.FrameHandler(args["folder"])
face.print_sequences()
face.select_sequence(1)
face.load_all_frames(50, 50)

nuke_animation = defaultdict(lambda: defaultdict(dict))

for frame in range(face.first_frame(), face.last_frame()+1,):
    print('Frame :{}'.format(frame))
    
    image = face.image(frame)

    img_width = face.image_dimensions(frame)[0]
    img_height = face.image_dimensions(frame)[1]

    # find landmarks
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(image)
    pprint(faces)
    #loop through results
    for face_detection in faces:
        # compute the (x, y)-coordinates of the bounding box for the
        startX, startY, width, height = face_detection['box']

        top_left      = Point(startX, startY, img_width, img_height)
        bottom_right  = Point(startX + width, startY + height, img_width, img_height)
        top_left.status()
        bottom_right.status()

        nuke_animation[frame]['x1'] = top_left.point_in_nuke()[0]
        nuke_animation[frame]['y1'] = top_left.point_in_nuke()[1]
        nuke_animation[frame]['x2'] = bottom_right.point_in_nuke()[0]
        nuke_animation[frame]['y2'] = bottom_right.point_in_nuke()[1]

        print(top_left.point_in_nuke())
        print(bottom_right.point_in_nuke())
        print('\n')

        crop =nnb.create_crop(top_left.point_in_nuke() + bottom_right.point_in_nuke())
        print(crop)
        
        # draw box around face
        cv2.rectangle(image, (startX, startY), (startX + width, startY + height),
            (0, 0, 255), 1) 
        cv2.imshow("Image with face drawn", image)
        cv2.waitKey(20)


# create animated curve
pprint(nuke_animation)
x1 = y1 = x2 = y2 = ''
for frame in nuke_animation:
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



# import folder contents of folder.
# process first frame for landmarks and store it.
# draw on frame these landmarks
# create nuke crop to match bounding box

# QS how do I keep track of a face it has found when there are others around it? - Facial Recognition  FaceNet

# possibly create tracker4 node with tracker animation matching landmarks.



