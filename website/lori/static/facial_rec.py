#from flask import render_template
from PIL import Image
import glob
import random
import os

PRES_SIZE = 10

"""
    Creates Trial 1 
    Part 1 includes 10 unique pairs of images.
    Part 2 includes 5 unique pairs of images with 5 images from Part 1

    @param zip_list list of unmasked-masked pairs
    @return pointer keeps track of index in zip_list
"""
def create_trial(zip_list):
    zip_pointer = PRES_SIZE

    trial1 = zip_list[:zip_pointer]
    random.shuffle(trial1)

    correct = trial1[:int(PRES_SIZE / 2)]

    trial2 = correct + zip_list[zip_pointer:int(zip_pointer + PRES_SIZE / 2)]
    random.shuffle(trial2)
    
    zip_pointer += int(PRES_SIZE / 2)

    return trial1, trial2, correct, zip_pointer

"""
    Extracts jpg images from masked file and jpeg images from unmasked file

    @return unmasked-masked image pairs
"""
def get_images():
    unmasked = []
    masked = []
    for path in sorted(glob.glob("website/lori/static/images/m/*")):
        filename = os.path.basename(path)
        masked.append(filename)
    for path in sorted(glob.glob("website/lori/static/images/_/*.jpeg")):
        filename = os.path.basename(path)
        unmasked.append(filename)
    zip_lists = list(zip(unmasked, masked))
    return zip_lists
    #return render_template("website/lori/templates/experiment.hmtl", unmasked=unmasked, masked=masked)

"""
    Creates both Trial 1 and 2
"""
def create_experiment():
    zip_lists = get_images()
    trial1_1, trial1_2, correct1, zip_pointer = create_trial(zip_lists)
    trial2_1, trial2_2, correct2, zip_pointer = create_trial(zip_lists[zip_pointer:])
    return trial1_1, trial1_2, correct1, trial2_1, trial2_2, correct2