# this is just in place to assist me building initial config file
# It could be used to recreate the json config file if it has been deleted.

import json
import os

nuke_config_json_file = os.path.join(os.path.dirname(__file__), 'nuke_config.json', )


# first value is frame number (int) the second is the value a float
frame_value = ' x{} {} '

# nuke animation curve format ready to take a string formatted using frame_value
animation_curve = '{{curve {} }}'

# ready for 4 curve strings or 4 floats to be inserted within box
# represents bottom left point and top right point
nuke_crop = """
Crop {{
    box {{ {} {} {} {} }}
    name Crop1
}}  
"""

nuke_tracker4 ='''
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


# create the dict to write out to our json file.
nuke_format_helpers = {
    'frame_value' : frame_value,
    'animation_curve' : animation_curve,
    'nuke_crop' : nuke_crop,
}

# Serializing json 
json_object = json.dumps(nuke_format_helpers, indent = 4)
  
# Writing to sample.json
with open(nuke_config_json_file, "w") as outfile:
    outfile.write(json_object)
print('JSON written to {}'.format(nuke_config_json_file))
