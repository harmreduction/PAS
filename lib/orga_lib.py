

import json
import os
dirname = os.path.dirname(__file__)
json_file = os.path.join(dirname, 'orga_lib.json')

def load_orga_lib():
    # load organization library
    with open(json_file, "r") as orgl:
        orga_dict = json.load(orgl)
    return orga_dict

