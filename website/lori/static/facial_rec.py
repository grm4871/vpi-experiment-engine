from flask import render_template
from PIL import Image
import glob

def get_images():
    unmasked = []
    masked = []
    for image in glob.glob("website/lori/static/images/m/*.jpg"):
        masked.append(Image.open(image))
    for image in glob.glob("website/lori/static/images/_/*.jpeg"):
        unmasked.append(Image.open(image))
    return render_template("website/lori/templates/experiment.hmtl", unmaksed=unmasked, masked=masked)