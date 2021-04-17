#from flask import render_template
from PIL import Image
import glob
import random

PRES_SIZE = 10

"""
    Combines each element of list1 and list2 into a tuple and 
    contains it all in a list

    @precondition list1 and list2 are equal length
    @return [(list1[0], list2[0]),(list1[1], list2[1])...]
"""
def zip_lists(list1, list2):
    zip_list = []
    
    for i in range(len(list1)):
        
        zip = (list1[i], list2[i])
        zip_list.append(zip)
    return zip_list

"""
    Creates Trial 1 
    Part 1 includes 10 unique pairs of images.
    Part 2 includes 5 unique pairs of images with 5 images from Part 1

    @param zip_list list of unmasked-masked pairs
    @return pointer keeps track of index in zip_list
"""
def create_trial1(zip_list):
    zip_pointer = PRES_SIZE

    trial1_1 = zip_list[:zip_pointer]
    random.shuffle(trial1_1)

    trial1_2 = trial1_1[:int(PRES_SIZE / 2)] + zip_list[zip_pointer:int(zip_pointer + PRES_SIZE / 2)]
    random.shuffle(trial1_2)
    
    zip_pointer += int(PRES_SIZE / 2)

    return trial1_1, trial1_2, zip_pointer

def create_trial2(zip_list):
    pass

def get_images():
    unmasked = []
    masked = []
    for image in glob.glob("website/lori/static/images/m/*.jpg"):
        masked.append(Image.open(image))
    for image in glob.glob("website/lori/static/images/_/*.jpeg"):
        unmasked.append(Image.open(image))
    zip = zip_lists(unmasked, masked)

    trial1_1, trial1_2, zip_pointer = create_trial1(zip)
    print(zip_pointer)
    
    #trial2_1, trial2_2 = create_trial2(zip[zip_pointer:])
    


    #return render_template("website/lori/templates/experiment.hmtl", unmasked=unmasked, masked=masked)

get_images()