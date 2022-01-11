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

from mtcnn import MTCNN
import numpy as np
import cv2

from point import Point
import loader


def nukeBuildCropNode(topleft_point, bottomright_point):
    crop_node = '''
Crop {{
box {{ {} {} {} {} }}
}}
'''.format(topleft_point[0], topleft_point[1], bottomright_point[0], bottomright_point[1])
    print(crop_node)
    return crop_node
    # below is the animation format for a nuke crop node
    #'''box {{{{curve x2 10 x20 0}} {{curve x2 10 x20 0}} {{curve x2 30 x20 0}} {{curve x2 30 x20 0}}}}'''

def nukeBuildTracker4Node():
    tracker_node = '''
    Tracker4 {{
    tracks {{ {{ 1 31 5 }} 
    {{ {{ 5 1 20 enable e 1 }} 
    {{ 3 1 75 name name 1 }} 
    {{ 2 1 58 track_x track_x 1 }} 
    {{ 2 1 58 track_y track_y 1 }} 
    {{ 2 1 63 offset_x offset_x 1 }} 
    {{ 2 1 63 offset_y offset_y 1 }} 
    {{ 4 1 27 T T 1 }} 
    {{ 4 1 27 R R 1 }} 
    {{ 4 1 27 S S 1 }} 
    {{ 2 0 45 error error 1 }} 
    {{ 1 1 0 error_min error_min 1 }} 
    {{ 1 1 0 error_max error_max 1 }} 
    {{ 1 1 0 pattern_x pattern_x 1 }} 
    {{ 1 1 0 pattern_y pattern_y 1 }} 
    {{ 1 1 0 pattern_r pattern_r 1 }} 
    {{ 1 1 0 pattern_t pattern_t 1 }} 
    {{ 1 1 0 search_x search_x 1 }} 
    {{ 1 1 0 search_y search_y 1 }} 
    {{ 1 1 0 search_r search_r 1 }} 
    {{ 1 1 0 search_t search_t 1 }} 
    {{ 2 1 0 key_track key_track 1 }} 
    {{ 2 1 0 key_search_x key_search_x 1 }} 
    {{ 2 1 0 key_search_y key_search_y 1 }} 
    {{ 2 1 0 key_search_r key_search_r 1 }} 
    {{ 2 1 0 key_search_t key_search_t 1 }} 
    {{ 2 1 0 key_track_x key_track_x 1 }} 
    {{ 2 1 0 key_track_y key_track_y 1 }} 
    {{ 2 1 0 key_track_r key_track_r 1 }} 
    {{ 2 1 0 key_track_t key_track_t 1 }} 
    {{ 2 1 0 key_centre_offset_x key_centre_offset_x 1 }} 
    {{ 2 1 0 key_centre_offset_y key_centre_offset_y 1 }} 
    }} 
    {{ 
    {{ {{curve K x20 1}} "left_eye" {{curve x20 563 x21 564}} {{curve x20 300}} {{curve K x20 0}} {{curve K x20 0}} 1 0 0 {{curve x20 0}} 0 0 -12 -12 12 12 -8 -8 8 8 {{}} {{curve x20 543}} {{curve x20 280}} {{curve x20 582}} {{curve x20 319}} {{curve x20 551}} {{curve x20 288}} {{curve x20 574}} {{curve x20 311}} {{curve x20 11.5}} {{curve x20 11.5}}  }} 
    {{ {{curve K x20 1}} "mouth_left" {{curve x20 577}} {{curve x20 223}} {{curve K x20 0}} {{curve K x20 0}} 0 0 0 {{curve x20 0}} 0 0 -12 -12 12 12 -8 -8 8 8 {{}} {{curve x20 557}} {{curve x20 203}} {{curve x20 596}} {{curve x20 242}} {{curve x20 565}} {{curve x20 211}} {{curve x20 588}} {{curve x20 234}} {{curve x20 11.5}} {{curve x20 11.5}}  }} 
    {{ {{curve K x20 1}} "mouth_right" {{curve x20 611}} {{curve x20 218}} {{curve K x20 0}} {{curve K x20 0}} 0 0 0 {{curve x20 0}} 0 0 -12 -12 12 12 -8 -8 8 8 {{}} {{curve x20 591}} {{curve x20 198}} {{curve x20 630}} {{curve x20 237}} {{curve x20 599}} {{curve x20 206}} {{curve x20 622}} {{curve x20 229}} {{curve x20 11.5}} {{curve x20 11.5}}  }} 
    {{ {{curve K x20 1}} "nose" {{curve x20 616}} {{curve x20 259}} {{curve K x20 0}} {{curve K x20 0}} 0 0 0 {{curve x20 0}} 0 0 -12 -12 12 12 -8 -8 8 8 {{}} {{curve x20 596}} {{curve x20 239}} {{curve x20 635}} {{curve x20 278}} {{curve x20 604}} {{curve x20 247}} {{curve x20 627}} {{curve x20 270}} {{curve x20 11.5}} {{curve x20 11.5}}  }} 
    {{ {{curve K x20 1}} "right_eye" {{curve x20 610}} {{curve x20 303}} {{curve K x20 0}} {{curve K x20 0}} 0 0 0 {{curve x20 0}} 0 0 -12 -12 12 12 -8 -8 8 8 {{}} {{curve x20 590}} {{curve x20 283}} {{curve x20 629}} {{curve x20 322}} {{curve x20 598}} {{curve x20 291}} {{curve x20 621}} {{curve x20 314}} {{curve x20 11.5}} {{curve x20 11.5}}  }} 
    }} 
    }}
    }}
    '''


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True, help="Path to the directory with")
args = vars(ap.parse_args())

face = loader.FrameHandler(args["folder"])

for frame in range(int(face.frame_range[0]), int(face.frame_range[1])+1):
    print('Frame :{}'.format(frame))
    image = face.file_sequence_data[frame]['image'] #cv2.imread(seqs.frame(frame))

    scale_percent = 20
    img_width = int(image.shape[1] * scale_percent / 100)
    img_height = int(image.shape[0] * scale_percent / 100)
    dim = (img_width, img_height)

    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    # find landmarks
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(resized)
    pprint(faces)

    #loop through results
    for face_detection in faces:
        # compute the (x, y)-coordinates of the bounding box for the
        startX, startY, width, height = face_detection['box']
        
        top_left      = Point(startX, startY, img_width, img_height)
        bottom_right  = Point(startX + width, startY + height, img_width, img_height)
        top_left.status()
        bottom_right.status()
        print(top_left.point_in_nuke())
        print(bottom_right.point_in_nuke())
        print('\n')
        #nukeBuildCropNode(top_left, bottom_right)
        nukeBuildCropNode(top_left.point_in_nuke(), bottom_right.point_in_nuke())
        # draw box around face
        cv2.rectangle(resized, (startX, startY), (startX + width, startY + height),
            (0, 0, 255), 1) 
        cv2.imshow("Image with face drawn", resized)
        cv2.waitKey(0)



# import folder contents of folder.
# process first frame for landmarks and store it.
# draw on frame these landmarks
# create nuke crop to match bounding box

# QS how do I keep track of a face it has found when there are others around it? - Facial Recognition  FaceNet

# possibly create tracker4 node with tracker animation matching landmarks.



