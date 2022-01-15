# this is just in place to assist me building initial config file
# It could be used to recreate the json config file if it has been deleted.

import json
import os

nuke_config_json_file = os.path.join(os.path.dirname(__file__), 'nuke_config.json', )


# first value is frame number (int) the second is the value a float
frame_value = """
 x{} {} 
"""

# nuke animation curve format ready to take a string formatted using frame_value
animation_curve = """
curve {{ {} }}
"""

# ready for 4 curve strings or 4 floats to be inserted within box
# represents bottom left point and top right point
nuke_crop = """
Crop {{
    box{{ {} {} {} {} }}
    name Crop1
}}  
"""


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
