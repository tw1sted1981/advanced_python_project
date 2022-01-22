# This class is to assist in creating the information required for 
# building nuke nodes.  It should handle creating animation syntax 
# and allow output of a .nk file or pasting into the clipboard.

# animation on curves is required to be sorted by frames or else the
# results are unexpected.  Lowest first to highest.

# might be best to build a data structure of a dict
# frame : value this and then sort by dict key



'''
wanting to build this format for a crop node
Crop {
    box {{curve x1 0 x20 308} {curve x1 0 x20 224} {curve x1 2048 x20 1596} {curve x1 1556 x20 1306}}
    name Crop1
}
'''


import os
import json

# load config file
nuke_config_json_file = os.path.join(os.path.dirname(__file__), 'nuke_config.json', )

with open(nuke_config_json_file, "r") as json_file:
    nuke_format_helpers = json.load(json_file)

def create_crop(nuke_list):    
    return nuke_format_helpers['nuke_crop'].format(*nuke_list)

def create_frame_value(frame, value):
    if value:
        frame_value = nuke_format_helpers['frame_value'].format(frame, value)
    else:
        frame_value = ''

    return frame_value 

def create_animation_curve(curve):
    return nuke_format_helpers['animation_curve'].format(curve)


def create_animated_crop(curve_list):
    return nuke_format_helpers['nuke_crop'].format(curve_list)


